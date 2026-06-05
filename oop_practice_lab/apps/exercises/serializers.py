"""DRF serializers for exercise catalog data."""
from rest_framework import serializers

from .models import Exercise, OOPConcept, TestCase


class OOPConceptSerializer(serializers.ModelSerializer):
    """Serialize OOP concept records."""

    class Meta:
        model = OOPConcept
        fields = ["id", "name"]


class TestCaseSerializer(serializers.ModelSerializer):
    """Serialize evaluator test case configuration."""

    class Meta:
        model = TestCase
        fields = ["id", "description", "check_type", "check_target", "check_args"]


class ExerciseSerializer(serializers.ModelSerializer):
    """Serialize exercises with concepts and optional test cases."""

    concepts = OOPConceptSerializer(many=True, read_only=True)
    test_cases = TestCaseSerializer(source="testcase_set", many=True, read_only=True)
    completed = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = [
            "id",
            "title",
            "description",
            "difficulty",
            "concepts",
            "starter_code",
            "expected_behavior",
            "created_at",
            "test_cases",
            "completed",
        ]

    def get_completed(self, obj):
        """Return whether the requesting user has completed the exercise."""
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return request.user.exercises_completed.filter(pk=obj.pk).exists()
