from rest_framework import serializers


class AIRecommendationRequestSerializer(serializers.Serializer):
    target_role = serializers.CharField(required=False, allow_blank=True, max_length=150)


class AIRecommendationResponseSerializer(serializers.Serializer):
    employee = serializers.DictField()
    target_role = serializers.CharField()
    current_skills = serializers.ListField()
    skill_gaps = serializers.ListField()
    certifications = serializers.ListField()
    recommendations = serializers.ListField()
    learning_roadmap = serializers.ListField()
