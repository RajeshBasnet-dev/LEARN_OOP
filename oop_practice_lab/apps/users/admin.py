"""Admin registration for custom users."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    """Expose learner fields in the Django admin."""

    fieldsets = UserAdmin.fieldsets + (
        ("Learning", {"fields": ("bio", "total_submissions", "exercises_completed")}),
    )
    filter_horizontal = ["groups", "user_permissions", "exercises_completed"]
    readonly_fields = ["total_submissions"]
