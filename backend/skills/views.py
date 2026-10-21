from rest_framework import viewsets

from .models import Skill, EmployeeSkill

from .serializers import (
    SkillSerializer,
    EmployeeSkillSerializer
)
from accounts.permissions import IsAdmin, IsAdminOrManager


class SkillViewSet(viewsets.ModelViewSet):

    queryset = Skill.objects.all().order_by("name")

    serializer_class = SkillSerializer

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsAdmin]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminOrManager]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]


class EmployeeSkillViewSet(viewsets.ModelViewSet):

    queryset = EmployeeSkill.objects.all().order_by("-id")

    serializer_class = EmployeeSkillSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        employee_id = self.request.query_params.get("employee")

        if employee_id:
            queryset = queryset.filter(employee_id=employee_id)

        return queryset

    def get_permissions(self):
        if self.action in ["create", "destroy", "update", "partial_update"]:
            permission_classes = [IsAdmin]
        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminOrManager]
        else:
            permission_classes = [IsAdmin]

        return [permission() for permission in permission_classes]