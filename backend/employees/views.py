from rest_framework import viewsets

from .models import Employee
from .serializers import EmployeeSerializer

from accounts.permissions import IsAdmin, IsAdminOrManager


class EmployeeViewSet(viewsets.ModelViewSet):

    queryset = Employee.objects.all().order_by("-id")
    serializer_class = EmployeeSerializer

    def get_permissions(self):

        if self.action in ["create", "destroy"]:
            permission_classes = [IsAdmin]

        elif self.action in ["list", "retrieve"]:
            permission_classes = [IsAdminOrManager]

        elif self.action in ["update", "partial_update"]:
            permission_classes = [IsAdmin]

        else:
            permission_classes = [IsAdmin]

        return [
            permission()
            for permission in permission_classes
        ]