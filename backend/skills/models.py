from django.db import models
from employees.models import Employee


class Skill(models.Model):

    name = models.CharField(max_length=100, unique=True)

    category = models.CharField(max_length=100)

    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class EmployeeSkill(models.Model):

    PROFICIENCY_CHOICES = [
        ("Beginner", "Beginner"),
        ("Intermediate", "Intermediate"),
        ("Advanced", "Advanced"),
        ("Expert", "Expert"),
    ]

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="skills"
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    proficiency = models.CharField(
        max_length=20,
        choices=PROFICIENCY_CHOICES
    )

    years_of_experience = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=0
    )

    last_used = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.skill.name}"

class Team(models.Model):

    name = models.CharField(max_length=100)

    manager = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class TeamSkillRequirement(models.Model):

    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE
    )

    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE
    )

    required_proficiency = models.CharField(
        max_length=20,
        choices=EmployeeSkill.PROFICIENCY_CHOICES
    )

    required_employees = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.team.name} - {self.skill.name}"