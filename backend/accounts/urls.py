"""URL declarations for account-related routes."""
from __future__ import annotations

from django.urls import path
from rest_framework_simplejwt.views import (  # type: ignore[import-untyped]
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    AccessibleLoginView,
    AccessibleLogoutView,
    PasswordChangeView,
    ProfileTemplateView,
    ProfileView,
    RegisterView,
    SignupView,
)

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password-change/", PasswordChangeView.as_view(), name="password-change"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", AccessibleLoginView.as_view(), name="login"),
    path("logout/", AccessibleLogoutView.as_view(), name="logout"),
    path("profile/page/", ProfileTemplateView.as_view(), name="profile-page"),
]
