"""Exercise API routes."""
from django.urls import path

from .views import ExerciseDetailAPIView, ExerciseListAPIView

urlpatterns = [
    path("", ExerciseListAPIView.as_view(), name="api-exercise-list"),
    path("<int:pk>/", ExerciseDetailAPIView.as_view(), name="api-exercise-detail"),
]
