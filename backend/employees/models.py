from django.db import models


class Employee(models.Model):

    employee_id = models.CharField(max_length=20, unique=True)

    name = models.CharField(max_length=100)

    email = models.EmailField(unique=True)

    department = models.CharField(max_length=100)

    designation = models.CharField(max_length=100)

    joining_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name