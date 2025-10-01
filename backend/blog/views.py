"""Presentation layer views for the blog."""
from __future__ import annotations

import json
from urllib.parse import urljoin

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.html import strip_tags
from django.utils.text import Truncator
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ai.services import AiSuggestionError, AiSuggestionService

from .forms import CommentForm, PostForm
from .models import Comment, Post, Tag


def _absolute_url(request: HttpRequest | None, value: str) -> str:
    if not value:
        return ""
    if value.startswith(("http://", "https://")):
        return value
    base = request.build_absolute_uri("/") if request else f"{settings.SITE_URL}/"
    return urljoin(base, value.lstrip("/"))


def _default_social_image(request: HttpRequest | None) -> str:
    candidate = (settings.SEO_DEFAULT_IMAGE or "").strip()
    if candidate:
        return _absolute_url(request, candidate)
    static_path = static("img/og-default.svg")
    return _absolute_url(request, static_path)


class PostListView(ListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"
    paginate_by = 9

    def get_queryset(self):
        queryset = (
            Post.objects.filter(status=Post.PUBLISHED)
            .select_related("author")
            .prefetch_related("tags")
            .order_by("-published_at", "-created_at")
        )
        search_term = self.request.GET.get("q")
        tag_slug = self.request.GET.get("tag")
        if search_term:
            queryset = queryset.filter(
                Q(title__icontains=search_term)
                | Q(summary__icontains=search_term)
                | Q(content__icontains=search_term)
            )
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        return queryset.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        request = self.request
        tags = Tag.objects.all()
        context["tags"] = tags

        search_term = request.GET.get("q", "")
        tag_slug = request.GET.get("tag")
        context["search_term"] = search_term
        context["active_tag"] = tag_slug

        tag_obj = tags.filter(slug=tag_slug).first() if tag_slug else None
        if tag_obj:
            meta_title = f"{tag_obj.name} posts - {settings.SITE_NAME}"
            description = f"Explore posts curated around {tag_obj.name} on {settings.SITE_NAME}."
        elif search_term:
            meta_title = f"Search results - {settings.SITE_NAME}"
            description = f"Results for '{search_term}' across {settings.SITE_NAME}'s AI-assisted publishing library."
        else:
            meta_title = f"Latest posts - {settings.SITE_NAME}"
            description = f"Discover the newest strategy guides, playbooks, and experiments from {settings.SITE_NAME}."

        context["meta_title"] = meta_title
        context["meta_description"] = description
        context.setdefault("canonical_url", request.build_absolute_uri())

        posts = list(context.get("object_list", []))
        items = []
        for index, post in enumerate(posts[:10], start=1):
            items.append(
                {
                    "@type": "ListItem",
                    "position": index,
                    "name": post.title,
                    "url": request.build_absolute_uri(post.get_absolute_url()),
                }
            )

        context["structured_data"] = [
            json.dumps(
                {
                    "@context": "https://schema.org",
                    "@type": "Blog",
                    "name": settings.SITE_NAME,
                    "url": settings.SITE_URL,
                    "description": settings.SITE_DESCRIPTION,
                    "inLanguage": "en",
                }
            ),
            json.dumps(
                {
                    "@context": "https://schema.org",
                    "@type": "ItemList",
                    "itemListElement": items,
                }
            ),
        ]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "blog/post_detail.html"
    context_object_name = "post"
    slug_field = "slug"

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author")
            .prefetch_related("tags", "comments__author")
            .filter(status__in=[Post.PUBLISHED, Post.DRAFT])
        )
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status=Post.PUBLISHED)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post: Post = context["post"]

        comment_form = kwargs.get("comment_form") or CommentForm()
        context["comment_form"] = comment_form
        context["comments"] = post.comments.filter(is_public=True).select_related("author")
        context["primary_tag"] = post.tags.first()

        ai_service = AiSuggestionService()
        try:
            context["seo_suggestions"] = ai_service.generate_seo_suggestions(
                title=post.title,
                summary=post.summary,
                content=post.content,
            )
        except AiSuggestionError as exc:
            context["seo_suggestions"] = []
            context["ai_error"] = str(exc)

        request = self.request
        summary_text = Truncator(strip_tags(post.summary)).chars(155)
        context["meta_title"] = f"{post.title} - {settings.SITE_NAME}"
        context["meta_description"] = summary_text
        context["open_graph_type"] = "article"
        context["meta_image"] = _default_social_image(request)
        context["canonical_url"] = request.build_absolute_uri(post.get_absolute_url())

        tags = list(post.tags.values_list("name", flat=True))
        keywords = ", ".join(tags) if tags else None
        published_at = post.published_at or post.created_at
        article_schema = {
            "@context": "https://schema.org",
            "@type": "BlogPosting",
            "headline": post.title,
            "description": summary_text,
            "author": {
                "@type": "Person",
                "name": getattr(post.author, "safe_display_name", str(post.author)),
            },
            "publisher": {
                "@type": "Organization",
                "name": settings.SITE_NAME,
                "url": settings.SITE_URL,
            },
            "mainEntityOfPage": context["canonical_url"],
            "image": context["meta_image"],
        }
        if published_at:
            article_schema["datePublished"] = published_at.isoformat()
        if post.updated_at:
            article_schema["dateModified"] = post.updated_at.isoformat()
        if keywords:
            article_schema["keywords"] = keywords

        breadcrumb_schema = {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": settings.SITE_URL},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{settings.SITE_URL}/"},
                {"@type": "ListItem", "position": 3, "name": post.title, "item": context["canonical_url"]},
            ],
        }
        context["structured_data"] = [json.dumps(article_schema), json.dumps(breadcrumb_schema)]
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        self.object = self.get_object()
        if not request.user.is_authenticated:
            messages.error(request, "Please sign in to add a comment.")
            return redirect("accounts:login")
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=self.object,
                author=request.user,
                body=form.cleaned_data["body"],
            )
            messages.success(request, "Comment posted successfully.")
            return redirect(self.object.get_absolute_url())
        context = self.get_context_data(comment_form=form)
        return self.render_to_response(context)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm
    success_url = reverse_lazy("blog:dashboard")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def form_valid(self, form: PostForm):
        post: Post = form.save(commit=False)
        post.author = self.request.user
        if post.status == Post.PUBLISHED and not post.published_at:
            post.published_at = timezone.now()
        post.save()
        form.save_m2m()
        messages.success(self.request, "Post created successfully.")
        return redirect(post.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.setdefault("meta_title", f"Create post - {settings.SITE_NAME}")
        context.setdefault("meta_description", f"Compose a new AI-ready story with {settings.SITE_NAME}'s editorial assistant.")
        context["meta_robots"] = "noindex, nofollow"
        return context


class PostUpdateView(LoginRequiredMixin, UpdateView):
    model = Post
    template_name = "blog/post_form.html"
    form_class = PostForm
    slug_field = "slug"

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.request.user
        return kwargs

    def get_queryset(self):
        queryset = Post.objects.filter(author=self.request.user)
        if self.request.user.is_staff:
            return Post.objects.all()
        return queryset

    def form_valid(self, form: PostForm):
        post: Post = form.save(commit=False)
        if post.status == Post.PUBLISHED and not post.published_at:
            post.published_at = timezone.now()
        elif post.status != Post.PUBLISHED:
            post.published_at = None
        post.save()
        form.save_m2m()
        messages.success(self.request, "Post updated successfully.")
        return redirect(post.get_absolute_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context.get("object") or getattr(self, "object", None)
        title = post.title if post else "post"
        context["meta_title"] = f"Edit {title} - {settings.SITE_NAME}"
        context["meta_description"] = f"Refine {title} with structured workflows and AI quality checks."
        context["meta_robots"] = "noindex, nofollow"
        return context


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    slug_field = "slug"
    success_url = reverse_lazy("blog:dashboard")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = context.get("object")
        title = post.title if post else "post"
        context["meta_title"] = f"Delete {title} - {settings.SITE_NAME}"
        context["meta_description"] = f"Confirm deletion for {title} and keep your catalogue tidy."
        context["meta_robots"] = "noindex, nofollow"
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            return Post.objects.all()
        return Post.objects.filter(author=self.request.user)

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Post deleted successfully.")
        return super().delete(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, ListView):
    template_name = "blog/dashboard.html"
    context_object_name = "posts"

    def get_queryset(self):
        return (
            Post.objects.filter(author=self.request.user)
            .select_related("author")
            .prefetch_related("tags")
            .order_by("-updated_at")
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = context.get("posts")
        queryset = posts if hasattr(posts, "filter") else self.get_queryset()
        context["draft_count"] = queryset.filter(status=Post.DRAFT).count()
        context["published_count"] = queryset.filter(status=Post.PUBLISHED).count()
        context["archived_count"] = queryset.filter(status=Post.ARCHIVED).count()
        context.setdefault("meta_title", f"Dashboard - {settings.SITE_NAME}")
        context.setdefault(
            "meta_description",
            "Review draft progress, track published stories, and unlock new optimisation opportunities.",
        )
        context["meta_robots"] = "noindex, nofollow"
        return context



