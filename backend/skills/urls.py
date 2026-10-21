from rest_framework.routers import DefaultRouter

from .views import (
    SkillViewSet,
    EmployeeSkillViewSet
)


router = DefaultRouter()

router.register(
    "skills",
    SkillViewSet,
    basename="skill"
)

router.register(
    "employee-skills",
    EmployeeSkillViewSet,
    basename="employee-skill"
)


urlpatterns = router.urls