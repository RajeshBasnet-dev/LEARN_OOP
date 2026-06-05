"""Submission and feedback persistence models."""
from django.conf import settings
from django.db import models

from apps.exercises.models import Exercise


class Submission(models.Model):
    """A student's code submission for one exercise."""

    STATUS = [("pending", "Pending"), ("evaluated", "Evaluated"), ("error", "Error")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    code = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS, default="pending")
    score = models.FloatField(null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        """Return a readable submission label."""
        return f"{self.user} → {self.exercise} ({self.score})"


class FeedbackItem(models.Model):
    """Structured evaluator feedback for a submission."""

    LEVEL = [
        ("pass", "Pass"),
        ("fail", "Fail"),
        ("warning", "Warning"),
        ("info", "Info"),
    ]

    submission = models.ForeignKey(
        Submission,
        on_delete=models.CASCADE,
        related_name="feedback",
    )
    level = models.CharField(max_length=10, choices=LEVEL)
    check_name = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        """Return a readable feedback label."""
        return f"{self.level}: {self.check_name}"
