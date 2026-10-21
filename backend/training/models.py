from django.db import models
from employees.models import Employee
from skills.models import Skill


class Training(models.Model):

    name = models.CharField(max_length=200)

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    provider = models.CharField(max_length=200)

    duration = models.CharField(max_length=100)

    training_url = models.URLField(blank=True)

    def __str__(self):
        return self.name


class TrainingRecommendation(models.Model):

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE
    )

    training = models.ForeignKey(
        Training,
        on_delete=models.CASCADE
    )

    reason = models.TextField()

    status = models.CharField(
        max_length=30,
        default="Recommended"
    )

    recommended_date = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.name} - {self.training.name}"