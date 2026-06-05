"""Models for OOP concepts, exercises, and AST-backed test cases."""
from django.db import models


class OOPConcept(models.Model):
    """A named object-oriented programming concept."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """Return the concept name."""
        return self.name


class Exercise(models.Model):
    """A programming prompt students solve in the Monaco editor."""

    DIFFICULTY = [("easy", "Easy"), ("medium", "Medium"), ("hard", "Hard")]

    title = models.CharField(max_length=200)
    description = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY)
    concepts = models.ManyToManyField(OOPConcept)
    starter_code = models.TextField()
    expected_behavior = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["difficulty", "created_at"]

    def __str__(self):
        """Return the exercise title."""
        return self.title


class TestCase(models.Model):
    """A data-driven evaluator check for an exercise."""

    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    check_type = models.CharField(max_length=50)
    check_target = models.CharField(max_length=100)
    check_args = models.JSONField(default=dict)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        """Return a readable test case label."""
        return f"{self.exercise}: {self.description}"
