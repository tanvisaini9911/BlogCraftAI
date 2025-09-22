"""API viewsets for the blog app."""
from __future__ import annotations

from django.db.models import Count, Prefetch, Q
from django.utils import timezone
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Comment, Post, Reaction, Tag
from .permissions import IsAuthorOrReadOnly, IsStaffOrReadOnly
from .serializers import CommentSerializer, PostSerializer, ReactionSerializer, TagSerializer


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    filterset_fields = ("status", "tags__slug")
    search_fields = ("title", "summary", "content", "tags__name")
    ordering_fields = ("published_at", "created_at", "title")

    def get_queryset(self):
        queryset = (
            Post.objects.select_related("author")
            .prefetch_related(
                "tags", Prefetch("comments", queryset=Comment.objects.filter(is_public=True))
            )
            .annotate(public_comment_count=Count("comments", filter=Q(comments__is_public=True)))
        )
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status=Post.PUBLISHED)
        elif self.request.query_params.get("mine") == "true":
            queryset = queryset.filter(author=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, slug=None):
        post: Post = self.get_object()
        if post.author != request.user and not request.user.is_staff:
            return Response({"detail": "Not allowed."}, status=status.HTTP_403_FORBIDDEN)
        post.status = Post.PUBLISHED
        post.published_at = timezone.now()
        post.save(update_fields=["status", "published_at"])
        serializer = self.get_serializer(post)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_queryset(self):
        queryset = Comment.objects.select_related("post", "author").filter(is_public=True)
        post_slug = self.request.query_params.get("post")
        if post_slug:
            queryset = queryset.filter(post__slug=post_slug)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TagViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsStaffOrReadOnly]
    lookup_field = "slug"
    search_fields = ("name",)
    ordering_fields = ("name",)


class ReactionViewSet(viewsets.ModelViewSet):
    serializer_class = ReactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reaction.objects.filter(user=self.request.user).select_related("post")

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reaction = serializer.save()
        headers = self.get_success_headers(serializer.data)
        response_serializer = self.get_serializer(reaction)
        return Response(response_serializer.data, status=status.HTTP_200_OK, headers=headers)
