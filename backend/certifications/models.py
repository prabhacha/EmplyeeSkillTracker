from django.db import models
from employees.models import Employee


class Certification(models.Model):

    name = models.CharField(max_length=200)

    issuing_organization = models.CharField(max_length=200)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EmployeeCertification(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    certification = models.ForeignKey(
        Certification,
        on_delete=models.CASCADE
    )

    certificate_number = models.CharField(
        max_length=100,
        blank=True
    )

    issue_date = models.DateField()

    expiry_date = models.DateField()

    document = models.FileField(
        upload_to="certificates/",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.certification.name}"