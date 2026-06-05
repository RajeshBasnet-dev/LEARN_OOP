"""Admin registrations for submissions."""
from django.contrib import admin

from .models import FeedbackItem, Submission


class FeedbackItemInline(admin.TabularInline):
    """Show evaluator feedback inline with a submission."""

    model = FeedbackItem
    extra = 0
    readonly_fields = ["level", "check_name", "message"]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    """Submission admin configuration."""

    list_display = ["user", "exercise", "status", "score", "submitted_at"]
    list_filter = ["status", "exercise"]
    search_fields = ["user__username", "exercise__title"]
    inlines = [FeedbackItemInline]
