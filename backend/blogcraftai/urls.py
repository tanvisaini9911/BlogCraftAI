"""URL configuration for BlogCraftAI."""
from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from blog.api import CommentViewSet, PostViewSet, ReactionViewSet, TagViewSet
from ai.api import SeoSuggestionView

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"reactions", ReactionViewSet, basename="reaction")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("api/", include((router.urls, "api"), namespace="api")),
    path("api/seo-suggestions/", SeoSuggestionView.as_view(), name="seo-suggestions"),
    path("", include("blog.urls", namespace="blog")),
]
