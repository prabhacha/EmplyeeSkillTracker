from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee
from accounts.permissions import IsAdminOrManager
from .serializers import AIRecommendationRequestSerializer
from .services import get_employee_context, generate_ai_recommendations


class AIRecommendationView(APIView):
    """
    POST /api/ai/recommend/<employee_id>/

    Body:
    {
        "target_role": "Python Full Stack Developer"
    }

    If target_role is omitted, the employee's current designation is used.
    """

    permission_classes = [IsAuthenticated, IsAdminOrManager]

    def post(self, request, employee_id):
        employee = Employee.objects.filter(
            id=employee_id,
            is_active=True,
        ).first()

        if not employee:
            return Response(
                {"error": "Active employee not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AIRecommendationRequestSerializer(
            data=request.data
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        target_role = (
            serializer.validated_data.get("target_role")
            or employee.designation
        )

        if not target_role:
            return Response(
                {
                    "error": (
                        "target_role is required when the employee "
                        "does not have a designation."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            context = get_employee_context(
                employee,
                target_role,
            )

            ai_result = generate_ai_recommendations(context)

            return Response(
                {
                    "employee": context["employee"],
                    "target_role": target_role,
                    "current_skills": context["current_skills"],
                    "skill_gaps": context["skill_gaps"],
                    "certifications": context["certifications"],
                    "training_catalogue": context["training_catalogue"],
                    "recommendations": ai_result.get(
                        "recommendations",
                        [],
                    ),
                    "learning_roadmap": ai_result.get(
                        "learning_roadmap",
                        [],
                    ),
                },
                status=status.HTTP_200_OK,
            )

        except RuntimeError as exc:
            return Response(
                {"error": str(exc)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )

        except Exception as exc:
            # Keep the actual server error out of the production response.
            # Django logging can be added here later.
            return Response(
                {
                    "error": "Unable to generate AI recommendations.",
                    "detail": str(exc),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
