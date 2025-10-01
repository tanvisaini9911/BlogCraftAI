"""URL configuration for BlogCraftAI."""
from __future__ import annotations

from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views.generic import TemplateView
from rest_framework import routers

from blog.api import CommentViewSet, PostViewSet, ReactionViewSet, TagViewSet
from blog.sitemaps import PostSitemap
from ai.api import SeoSuggestionView

router = routers.DefaultRouter()
router.register(r"posts", PostViewSet, basename="post")
router.register(r"comments", CommentViewSet, basename="comment")
router.register(r"tags", TagViewSet, basename="tag")
router.register(r"reactions", ReactionViewSet, basename="reaction")

sitemaps = {"posts": PostSitemap()}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls", namespace="accounts")),
    path("api/", include((router.urls, "api"), namespace="api")),
    path("api/seo-suggestions/", SeoSuggestionView.as_view(), name="seo-suggestions"),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("", include("blog.urls", namespace="blog")),
]
