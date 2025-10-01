"""Views for managing account workflows."""
from __future__ import annotations

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views
from django.utils.http import url_has_allowed_host_and_scheme
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("meta_title", f"Register - {settings.SITE_NAME}")
        context.setdefault("meta_description", f"Create a {settings.SITE_NAME} account to collaborate with AI-assisted editorial tools.")
        context["meta_robots"] = "noindex, nofollow"
        return context

    def form_valid(self, form: SignupForm):
        form.save()
        messages.success(self.request, "Account created successfully. You can now sign in.")
        return super().form_valid(form)


class ProfileTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "accounts/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("meta_title", f"Your profile - {settings.SITE_NAME}")
        context.setdefault("meta_description", "Update your display name, avatar, and bio for personalised attribution.")
        context["meta_robots"] = "noindex, nofollow"
        return context

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("meta_title", f"Sign in - {settings.SITE_NAME}")
        context.setdefault("meta_description", f"Access your {settings.SITE_NAME} projects and analytics with a secure login.")
        context["meta_robots"] = "noindex, nofollow"
        return context


class AccessibleLogoutView(TemplateView):
    template_name = "accounts/logged_out.html"
    http_method_names = ["get", "post", "head", "options"]
    default_redirect = reverse_lazy("blog:post-list")

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            logout(request)
            messages.success(request, "You have been signed out.")
        else:
            messages.info(request, "You were already signed out.")
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return self.render_to_response(self.get_context_data(**kwargs))

    def post(self, request, *args, **kwargs):
        return redirect(self._resolve_redirect_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["redirect_url"] = self._resolve_redirect_url()
        context.setdefault("meta_title", f"Signed out - {settings.SITE_NAME}")
        context.setdefault("meta_description", f"You have been signed out safely from {settings.SITE_NAME}.")
        context["meta_robots"] = "noindex, nofollow"
        return context

    def _resolve_redirect_url(self) -> str:
        candidate = self.request.GET.get("next") or self.request.POST.get("next")
        allowed_hosts = {self.request.get_host()}
        allowed_hosts.update(host for host in settings.ALLOWED_HOSTS if host)
        if candidate and url_has_allowed_host_and_scheme(
            candidate,
            allowed_hosts=allowed_hosts,
            allowed_schemes={"http", "https"},
        ):
            return candidate
        return str(self.default_redirect)


