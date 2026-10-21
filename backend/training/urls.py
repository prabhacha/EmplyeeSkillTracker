from rest_framework.routers import DefaultRouter

from .views import (
    TrainingViewSet,
    TrainingRecommendationViewSet
)


router = DefaultRouter()

router.register(
    "trainings",
    TrainingViewSet,
    basename="training"
)

router.register(
    "recommendations",
    TrainingRecommendationViewSet,
    basename="recommendation"
)


urlpatterns = router.urls