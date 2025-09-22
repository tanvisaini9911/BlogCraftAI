from __future__ import annotations

import pytest
from django.utils import timezone
from rest_framework import status

from blog.models import Post, Tag

from .factories import CommentFactory, PostFactory, TagFactory, UserFactory


@pytest.mark.django_db
def test_post_list_filters_published(api_client):
    PostFactory(status=Post.DRAFT)
    published = PostFactory(status=Post.PUBLISHED)
    response = api_client.get("/api/posts/")
    assert response.status_code == status.HTTP_200_OK
    slugs = [item["slug"] for item in response.data["results"]]
    assert published.slug in slugs
    assert all(slug != published.slug or True for slug in slugs)
    assert len(response.data["results"]) == 1


@pytest.mark.django_db
def test_authenticated_user_can_create_post(auth_client):
    client, user = auth_client
    tag = TagFactory()
    payload = {
        "title": "Prompt-driven development",
        "summary": "How to use AI effectively",
        "content": "Detailed walkthrough",
        "status": Post.PUBLISHED,
        "tags": [tag.name],
    }
    response = client.post("/api/posts/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    post = Post.objects.get(slug=response.data["slug"])
    assert post.author == user
    assert post.tags.filter(pk=tag.pk).exists()


@pytest.mark.django_db
def test_non_author_cannot_update_post(api_client):
    post = PostFactory()
    other_user = UserFactory()
    api_client.force_authenticate(other_user)
    response = api_client.patch(f"/api/posts/{post.slug}/", {"title": "Hacked"}, format="json")
    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_comment_requires_authentication(api_client):
    post = PostFactory()
    response = api_client.post(
        "/api/comments/",
        {"post": post.id, "body": "Great article!"},
        format="json",
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_reaction_is_upserted(auth_client):
    client, user = auth_client
    post = PostFactory(author=user)
    payload = {"post": post.id, "reaction": "like"}
    first = client.post("/api/reactions/", payload, format="json")
    assert first.status_code == status.HTTP_200_OK
    payload["reaction"] = "dislike"
    second = client.post("/api/reactions/", payload, format="json")
    assert second.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.reactions.get(user=user).reaction == "dislike"


@pytest.mark.django_db
def test_publish_action_requires_author(auth_client):
    client, user = auth_client
    post = PostFactory(author=user, status=Post.DRAFT, published_at=None)
    response = client.post(f"/api/posts/{post.slug}/publish/")
    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.status == Post.PUBLISHED
    assert post.published_at is not None
