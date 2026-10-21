from django.urls import path

from .views import AIRecommendationView


urlpatterns = [
    path(
        "recommend/<int:employee_id>/",
        AIRecommendationView.as_view(),
        name="ai-recommendation",
    ),
]
