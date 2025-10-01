"""Admin registration for blog models."""
from __future__ import annotations

from django.contrib import admin

from .models import Comment, Post, Reaction, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "status", "author", "published_at")
    list_filter = ("status", "tags")
    search_fields = ("title", "summary", "content")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [CommentInline]
    autocomplete_fields = ("author", "tags")


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "is_public", "created_at")
    list_filter = ("is_public",)
    search_fields = ("body", "author__email")


@admin.register(Reaction)
class ReactionAdmin(admin.ModelAdmin):
    list_display = ("post", "user", "reaction", "created_at")
    list_filter = ("reaction",)
    autocomplete_fields = ("post", "user")
