"""Exercises app configuration."""
from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    """Configure the exercises application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.exercises"
    label = "exercises"
