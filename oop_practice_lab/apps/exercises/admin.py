"""Admin registrations for exercise authoring."""
from django.contrib import admin

from .models import Exercise, OOPConcept, TestCase


class TestCaseInline(admin.TabularInline):
    """Edit test cases alongside exercises."""

    model = TestCase
    extra = 1


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    """Exercise admin configuration."""

    list_display = ["title", "difficulty", "created_at"]
    list_filter = ["difficulty", "concepts"]
    search_fields = ["title", "description"]
    inlines = [TestCaseInline]


@admin.register(OOPConcept)
class OOPConceptAdmin(admin.ModelAdmin):
    """Concept admin configuration."""

    search_fields = ["name"]
