"""URL configuration for OOP Practice Lab."""
from django.contrib import admin
from django.urls import include, path

from apps.exercises.views import EditorView, ExerciseDetailView, HomeView, ResultView
from apps.submissions.views import DashboardAPIView, DashboardView
from apps.users.views import RegisterView, UserLoginView, UserLogoutView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", HomeView.as_view(), name="home"),
    path("exercises/<int:pk>/", ExerciseDetailView.as_view(), name="exercise-detail"),
    path("exercises/<int:pk>/editor/", EditorView.as_view(), name="editor"),
    path("results/<int:pk>/", ResultView.as_view(), name="result"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("api/auth/", include("apps.users.urls")),
    path("api/exercises/", include("apps.exercises.urls")),
    path("api/submissions/", include("apps.submissions.urls")),
    path("api/dashboard/", DashboardAPIView.as_view(), name="api-dashboard"),
]
