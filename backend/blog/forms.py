"""Forms for HTML-based blog interactions."""
from __future__ import annotations

from django import forms

from .models import Comment, Post, Tag


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ("title", "summary", "content", "status", "tags")
        widgets = {
            "summary": forms.Textarea(attrs={"rows": 3}),
            "content": forms.Textarea(attrs={"rows": 8}),
            "tags": forms.CheckboxSelectMultiple,
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)
        self.fields["tags"].queryset = Tag.objects.order_by("name")
        if user and not user.is_staff:
            self.fields["status"].choices = [(Post.DRAFT, "Draft"), (Post.PUBLISHED, "Published")]


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ("body",)
        widgets = {"body": forms.Textarea(attrs={"rows": 3, "aria-label": "Comment text"})}
