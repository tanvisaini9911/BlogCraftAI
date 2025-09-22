"""Views for managing account workflows."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, TemplateView
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .forms import SignupForm
from .serializers import PasswordChangeSerializer, RegistrationSerializer, UserSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer

    def get_object(self) -> User:
        return self.request.user

    def get_permissions(self):
        if self.request.method in ("GET", "HEAD", "OPTIONS"):
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]


class PasswordChangeView(generics.UpdateAPIView):
    serializer_class = PasswordChangeSerializer

    def get_object(self) -> User:
        return self.request.user

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SignupView(FormView):
    template_name = "accounts/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy("accounts:login")

    def form_valid(self, form: SignupForm):
        form.save()
        messages.success(self.request, "Account created successfully. You can now sign in.")
        return super().form_valid(form)


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def post(self, request, *args, **kwargs):
        # Allow profile updates from HTML form in addition to API usage.
        user = request.user
        user.display_name = request.POST.get("display_name", user.display_name)
        user.bio = request.POST.get("bio", user.bio)
        user.avatar_url = request.POST.get("avatar_url", user.avatar_url)
        user.full_clean()
        user.save(update_fields=["display_name", "bio", "avatar_url"])
        messages.success(request, "Profile updated successfully.")
        return redirect("accounts:profile-page")


class AccessibleLoginView(auth_views.LoginView):
    template_name = "accounts/login.html"
    redirect_authenticated_user = True


class AccessibleLogoutView(auth_views.LogoutView):
    template_name = "accounts/logged_out.html"
