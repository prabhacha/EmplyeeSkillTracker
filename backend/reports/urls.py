from django.urls import path

from .views import SkillMatrixView


urlpatterns = [
    path("reports/skill-matrix/", SkillMatrixView.as_view(), name="skill-matrix"),
]
