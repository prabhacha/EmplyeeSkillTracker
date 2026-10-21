from rest_framework import serializers

from .models import (
    Certification,
    EmployeeCertification
)


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = "__all__"


class EmployeeCertificationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = EmployeeCertification
        fields = "__all__"