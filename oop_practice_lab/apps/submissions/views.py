"""Views for submission APIs and learner dashboards."""
from collections import defaultdict

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg
from django.views.generic import TemplateView
from rest_framework import generics, permissions, response, status, views

from apps.evaluator.engine import OOPEvaluator
from apps.exercises.models import OOPConcept

from .models import FeedbackItem, Submission
from .serializers import SubmissionCreateSerializer, SubmissionSerializer


class SubmissionListCreateAPIView(generics.ListCreateAPIView):
    """List a user's submissions or evaluate a new submission."""

    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Use a smaller serializer for incoming submissions."""
        if self.request.method == "POST":
            return SubmissionCreateSerializer
        return SubmissionSerializer

    def get_queryset(self):
        """Return only submissions owned by the requesting user."""
        return Submission.objects.filter(user=self.request.user).select_related(
            "exercise"
        ).prefetch_related("feedback", "exercise__concepts")

    def create(self, request, *args, **kwargs):
        """Create, evaluate, score, and return a code submission."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save(user=request.user, status="pending")

        evaluator = OOPEvaluator()
        test_cases = submission.exercise.testcase_set.all()
        results = evaluator.evaluate(submission.code, test_cases)
        total = len(results)
        passed = sum(1 for item in results if item.passed)

        FeedbackItem.objects.bulk_create(
            [
                FeedbackItem(
                    submission=submission,
                    level=item.level,
                    check_name=item.check_name,
                    message=item.message,
                )
                for item in results
            ]
        )
        submission.score = passed / total if total else 0.0
        submission.status = "evaluated"
        submission.save(update_fields=["score", "status"])

        if submission.score >= 0.8:
            request.user.exercises_completed.add(submission.exercise)

        output = SubmissionSerializer(submission, context={"request": request})
        headers = self.get_success_headers(output.data)
        return response.Response(output.data, status=status.HTTP_201_CREATED, headers=headers)


class SubmissionDetailAPIView(generics.RetrieveAPIView):
    """Return a single owned submission with feedback."""

    serializer_class = SubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Return only submissions owned by the requesting user."""
        return Submission.objects.filter(user=self.request.user).select_related(
            "exercise"
        ).prefetch_related("feedback", "exercise__concepts")


class DashboardAPIView(views.APIView):
    """Return aggregated learner statistics and concept progress."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """Build dashboard metrics for the authenticated user."""
        submissions = Submission.objects.filter(user=request.user).prefetch_related(
            "exercise__concepts"
        )
        average = submissions.aggregate(avg=Avg("score"))["avg"] or 0.0
        progress = defaultdict(lambda: {"attempted": 0, "passed": 0})

        for submission in submissions:
            for concept in submission.exercise.concepts.all():
                progress[concept.name]["attempted"] += 1
                if submission.score is not None and submission.score >= 0.8:
                    progress[concept.name]["passed"] += 1

        for concept in OOPConcept.objects.all():
            progress[concept.name]

        payload = {
            "total_submissions": request.user.total_submissions,
            "exercises_completed": request.user.exercises_completed.count(),
            "avg_score": round(average, 2),
            "concept_progress": dict(progress),
        }
        return response.Response(payload)


class DashboardView(LoginRequiredMixin, TemplateView):
    """Render dashboard stats and submission history."""

    template_name = "dashboard.html"

    def get_context_data(self, **kwargs):
        """Add summary metrics and concept percentages."""
        context = super().get_context_data(**kwargs)
        submissions = Submission.objects.filter(user=self.request.user).select_related(
            "exercise"
        ).prefetch_related("exercise__concepts", "feedback")
        average = submissions.aggregate(avg=Avg("score"))["avg"] or 0.0
        progress = defaultdict(lambda: {"attempted": 0, "passed": 0, "percent": 0})
        for submission in submissions:
            for concept in submission.exercise.concepts.all():
                progress[concept.name]["attempted"] += 1
                if submission.score is not None and submission.score >= 0.8:
                    progress[concept.name]["passed"] += 1
        for concept, values in progress.items():
            if values["attempted"]:
                values["percent"] = round(values["passed"] / values["attempted"] * 100)
        context.update(
            {
                "total_submissions": self.request.user.total_submissions,
                "completed_count": self.request.user.exercises_completed.count(),
                "avg_score": round(average * 100),
                "concept_progress": dict(progress),
                "submissions": submissions,
            }
        )
        return context
