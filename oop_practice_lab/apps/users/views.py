"""Authentication API and template views."""
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.views.generic import CreateView
from rest_framework import permissions, response, status, views

from .serializers import LoginSerializer, RegisterSerializer, UserProfileSerializer


class RegisterAPIView(views.APIView):
    """Create an account and sign the user in."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Register a new user via the API."""
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        login(request, user)
        return response.Response(
            UserProfileSerializer(user).data,
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(views.APIView):
    """Authenticate an existing user."""

    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Log a user in via session authentication."""
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return response.Response(UserProfileSerializer(user).data)


class LogoutAPIView(views.APIView):
    """End the authenticated user's session."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Log a user out via the API."""
        logout(request)
        return response.Response(status=status.HTTP_204_NO_CONTENT)


class RegisterView(CreateView):
    """Render and process the HTML registration form."""

    serializer_class = RegisterSerializer
    template_name = "auth/register.html"

    def get(self, request, *args, **kwargs):
        """Display the registration form."""
        return self.render_to_response({})

    def post(self, request, *args, **kwargs):
        """Validate the registration form and sign in the new user."""
        serializer = RegisterSerializer(data=request.POST)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return redirect("home")
        return self.render_to_response({"errors": serializer.errors})


class UserLoginView(LoginView):
    """Render and process the HTML login form."""

    template_name = "auth/login.html"


class UserLogoutView(LogoutView):
    """Log the current user out from the HTML interface."""

    http_method_names = ["post"]
