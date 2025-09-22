"""REST API serializers for the blog app."""
from __future__ import annotations

from django.utils import timezone
from rest_framework import serializers

from accounts.serializers import UserSerializer

from .models import Comment, Post, Reaction, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("id", "name", "slug")
        read_only_fields = ("id", "slug")


class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    tags = serializers.SlugRelatedField(
        many=True,
        slug_field="name",
        queryset=Tag.objects.all(),
        required=False,
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "title",
            "slug",
            "summary",
            "content",
            "status",
            "tags",
            "published_at",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "slug", "created_at", "updated_at", "author")

    def validate(self, attrs: dict) -> dict:
        status = attrs.get("status", getattr(self.instance, "status", Post.DRAFT))
        published_at = attrs.get("published_at", getattr(self.instance, "published_at", None))
        if status == Post.PUBLISHED and published_at is None:
            attrs["published_at"] = timezone.now()
        if status != Post.PUBLISHED and published_at:
            attrs["published_at"] = None
        return attrs

    def create(self, validated_data: dict) -> Post:
        tags = validated_data.pop("tags", [])
        author = validated_data.pop("author", self.context["request"].user)
        post = Post.objects.create(author=author, **validated_data)
        if tags:
            self._sync_tags(post, tags)
        return post

    def update(self, instance: Post, validated_data: dict) -> Post:
        tags = validated_data.pop("tags", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if tags is not None:
            self._sync_tags(instance, tags)
        return instance

    def _sync_tags(self, post: Post, tags: list[Tag]) -> None:
        tag_objects: list[Tag] = []
        for tag in tags:
            if isinstance(tag, Tag):
                tag_objects.append(tag)
            else:
                tag_objects.append(Tag.objects.get_or_create(name=tag)[0])
        post.tags.set(tag_objects)


class CommentSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "post",
            "author",
            "body",
            "parent",
            "is_public",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "author", "created_at", "updated_at")

    def create(self, validated_data: dict) -> Comment:
        request = self.context["request"]
        validated_data["author"] = request.user
        return super().create(validated_data)


class ReactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reaction
        fields = ("id", "post", "reaction", "created_at")
        read_only_fields = ("id", "created_at")

    def create(self, validated_data: dict) -> Reaction:
        request = self.context["request"]
        reaction, _ = Reaction.objects.update_or_create(
            user=request.user,
            post=validated_data["post"],
            defaults={"reaction": validated_data["reaction"]},
        )
        return reaction
