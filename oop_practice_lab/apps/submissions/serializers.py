"""DRF serializers for submissions and feedback."""
from rest_framework import serializers

from apps.exercises.serializers import ExerciseSerializer

from .models import FeedbackItem, Submission


class FeedbackItemSerializer(serializers.ModelSerializer):
    """Serialize a single evaluator feedback item."""

    class Meta:
        model = FeedbackItem
        fields = ["id", "level", "check_name", "message"]


class SubmissionSerializer(serializers.ModelSerializer):
    """Serialize submissions with nested feedback."""

    feedback = FeedbackItemSerializer(many=True, read_only=True)
    exercise_detail = ExerciseSerializer(source="exercise", read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "exercise",
            "exercise_detail",
            "code",
            "status",
            "score",
            "submitted_at",
            "feedback",
        ]
        read_only_fields = ["status", "score", "submitted_at", "feedback"]


class SubmissionCreateSerializer(serializers.ModelSerializer):
    """Validate incoming code submissions."""

    class Meta:
        model = Submission
        fields = ["exercise", "code"]
