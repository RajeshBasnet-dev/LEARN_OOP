"""Custom user model for learner profile data."""
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.exercises.models import Exercise


class UserProfile(AbstractUser):
    """Application user with learning progress fields."""

    bio = models.TextField(blank=True)
    total_submissions = models.IntegerField(default=0)
    exercises_completed = models.ManyToManyField(Exercise, blank=True)

    def __str__(self):
        """Return the user's username."""
        return self.username
