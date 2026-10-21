from rest_framework import viewsets

from .models import (
    Certification,
    EmployeeCertification
)

from .serializers import (
    CertificationSerializer,
    EmployeeCertificationSerializer
)


class CertificationViewSet(viewsets.ModelViewSet):

    queryset = Certification.objects.all().order_by("name")

    serializer_class = CertificationSerializer


class EmployeeCertificationViewSet(
    viewsets.ModelViewSet
):

    queryset = EmployeeCertification.objects.all().order_by(
        "expiry_date"
    )

    serializer_class = EmployeeCertificationSerializer