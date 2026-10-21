from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from employees.models import Employee


class SkillMatrixView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		employees = Employee.objects.prefetch_related(
			"skills__skill"
		).order_by("name")

		matrix = []

		for employee in employees:
			matrix.append({
				"id": employee.id,
				"name": employee.name,
				"skills": {
					employee_skill.skill.name: employee_skill.proficiency
					for employee_skill in employee.skills.all()
				}
			})

		return Response(matrix)
