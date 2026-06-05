"""Submission API routes."""
from django.urls import path

from .views import DashboardAPIView, SubmissionDetailAPIView, SubmissionListCreateAPIView

urlpatterns = [
    path("", SubmissionListCreateAPIView.as_view(), name="api-submission-list-create"),
    path("<int:pk>/", SubmissionDetailAPIView.as_view(), name="api-submission-detail"),
    path("dashboard/", DashboardAPIView.as_view(), name="api-dashboard-nested"),
]
