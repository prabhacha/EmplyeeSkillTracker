from rest_framework import viewsets

from .models import (
    Training,
    TrainingRecommendation
)

from .serializers import (
    TrainingSerializer,
    TrainingRecommendationSerializer
)


class TrainingViewSet(viewsets.ModelViewSet):

    queryset = Training.objects.all().order_by("name")

    serializer_class = TrainingSerializer


class TrainingRecommendationViewSet(
    viewsets.ModelViewSet
):

    queryset = TrainingRecommendation.objects.all().order_by(
        "-recommended_date"
    )

    serializer_class = TrainingRecommendationSerializer