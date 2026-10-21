from rest_framework import serializers

from .models import (
    Training,
    TrainingRecommendation
)


class TrainingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Training
        fields = "__all__"


class TrainingRecommendationSerializer(
    serializers.ModelSerializer
):

    class Meta:
        model = TrainingRecommendation
        fields = "__all__"