from rest_framework.routers import DefaultRouter

from .views import (
    CertificationViewSet,
    EmployeeCertificationViewSet
)


router = DefaultRouter()

router.register(
    "certifications",
    CertificationViewSet,
    basename="certification"
)

router.register(
    "employee-certifications",
    EmployeeCertificationViewSet,
    basename="employee-certification"
)


urlpatterns = router.urls