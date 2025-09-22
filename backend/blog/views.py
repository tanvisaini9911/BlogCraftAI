"""Presentation layer views for the blog."""
from __future__ import annotations

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import DetailView, ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from ai.services import AiSuggestionError, AiSuggestionService

from .forms import CommentForm, PostForm
from .models import Comment, Post, Tag


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
        context["tags"] = Tag.objects.all()
        context["search_term"] = self.request.GET.get("q", "")
        context["active_tag"] = self.request.GET.get("tag")
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
        context["comment_form"] = CommentForm()
        context["comments"] = post.comments.filter(is_public=True).select_related("author")
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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    slug_field = "slug"
    success_url = reverse_lazy("blog:dashboard")

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
        context["draft_count"] = self.get_queryset().filter(status=Post.DRAFT).count()
        context["published_count"] = self.get_queryset().filter(status=Post.PUBLISHED).count()
        context["archived_count"] = self.get_queryset().filter(status=Post.ARCHIVED).count()
        return context
