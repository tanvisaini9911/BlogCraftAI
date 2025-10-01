from __future__ import annotations

import pytest
from django.urls import reverse

from ai.services import AiSuggestionService
from blog.models import Post

from .factories import PostFactory, UserFactory


@pytest.mark.django_db
def test_post_list_page_renders(client):
    PostFactory.create_batch(3)
    response = client.get(reverse("blog:post-list"))
    assert response.status_code == 200
    assert b"Discover AI-assisted writing" in response.content


@pytest.mark.django_db
def test_post_detail_shows_ai_suggestions(monkeypatch, client):
    post = PostFactory()

    def fake_suggestions(**kwargs):
        return []

    monkeypatch.setattr(AiSuggestionService, "generate_seo_suggestions", staticmethod(fake_suggestions))
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
    assert b"AI SEO suggestions" in response.content


@pytest.mark.django_db
def test_comment_submission_requires_login(client):
    post = PostFactory()
    response = client.post(post.get_absolute_url(), {"body": "Nice"})
    assert response.status_code == 302
    assert reverse("accounts:login") in response["Location"]


@pytest.mark.django_db
def test_author_can_view_draft(client):
    author = UserFactory()
    post = PostFactory(author=author, status=Post.DRAFT)
    client.force_login(author)
    response = client.get(post.get_absolute_url())
    assert response.status_code == 200
