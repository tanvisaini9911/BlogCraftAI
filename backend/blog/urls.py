"""URL declarations for the blog presentation layer."""
from __future__ import annotations

from django.urls import path

from .views import (
    DashboardView,
    PostCreateView,
    PostDeleteView,
    PostDetailView,
    PostListView,
    PostUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("posts/new/", PostCreateView.as_view(), name="post-create"),
    path("posts/<slug:slug>/", PostDetailView.as_view(), name="post-detail"),
    path("posts/<slug:slug>/edit/", PostUpdateView.as_view(), name="post-update"),
    path("posts/<slug:slug>/delete/", PostDeleteView.as_view(), name="post-delete"),
]
