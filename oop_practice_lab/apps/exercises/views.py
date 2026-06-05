"""Views for exercise APIs and learning pages."""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, ListView, TemplateView
from rest_framework import generics, permissions

from .models import Exercise, OOPConcept
from .serializers import ExerciseSerializer


class ExerciseListAPIView(generics.ListAPIView):
    """Return all exercises; public read-only endpoint."""

    serializer_class = ExerciseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        """Filter exercises by difficulty and concept query parameters."""
        queryset = Exercise.objects.prefetch_related("concepts", "testcase_set")
        difficulty = self.request.query_params.get("difficulty")
        concept = self.request.query_params.get("concept")
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if concept:
            queryset = queryset.filter(concepts__name=concept)
        return queryset.distinct()


class ExerciseDetailAPIView(generics.RetrieveAPIView):
    """Return one exercise and its evaluator test cases."""

    queryset = Exercise.objects.prefetch_related("concepts", "testcase_set")
    serializer_class = ExerciseSerializer
    permission_classes = [permissions.AllowAny]


class HomeView(ListView):
    """Render the filterable exercise catalog page."""

    model = Exercise
    template_name = "home.html"
    context_object_name = "exercises"

    def get_queryset(self):
        """Filter exercises by difficulty and concept query parameters."""
        queryset = Exercise.objects.prefetch_related("concepts")
        difficulty = self.request.GET.get("difficulty")
        concept = self.request.GET.get("concept")
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)
        if concept:
            queryset = queryset.filter(concepts__name=concept)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        """Add filter options and completed exercise IDs."""
        context = super().get_context_data(**kwargs)
        context["concepts"] = OOPConcept.objects.all()
        context["selected_difficulty"] = self.request.GET.get("difficulty", "")
        context["selected_concept"] = self.request.GET.get("concept", "")
        if self.request.user.is_authenticated:
            context["completed_ids"] = set(
                self.request.user.exercises_completed.values_list("id", flat=True)
            )
        else:
            context["completed_ids"] = set()
        return context


class ExerciseDetailView(DetailView):
    """Render an exercise overview page."""

    model = Exercise
    template_name = "exercise_detail.html"
    context_object_name = "exercise"

    def get_queryset(self):
        """Fetch exercises with related concepts and tests."""
        return Exercise.objects.prefetch_related("concepts", "testcase_set")


class EditorView(LoginRequiredMixin, DetailView):
    """Render the Monaco editor for an exercise."""

    model = Exercise
    template_name = "editor.html"
    context_object_name = "exercise"


class ResultView(LoginRequiredMixin, TemplateView):
    """Render a submission result page by ID."""

    template_name = "result.html"

    def get_context_data(self, **kwargs):
        """Add the owned submission to template context."""
        from apps.submissions.models import Submission

        context = super().get_context_data(**kwargs)
        context["submission"] = get_object_or_404(
            Submission.objects.select_related("exercise").prefetch_related("feedback"),
            pk=kwargs["pk"],
            user=self.request.user,
        )
        submission = context["submission"]
        context["score_percent"] = round((submission.score or 0) * 100)
        completed_ids = self.request.user.exercises_completed.values_list(
            "pk", flat=True
        )
        context["next_exercise"] = (
            Exercise.objects.exclude(pk__in=[submission.exercise_id, *completed_ids])
            .order_by("id")
            .first()
        )
        return context
