"""Submissions app configuration."""
from django.apps import AppConfig


class SubmissionsConfig(AppConfig):
    """Configure the submissions application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.submissions"
    label = "submissions"

    def ready(self):
        """Import signals once the app registry is ready."""
        from . import signals  # noqa: F401
