"""Pytest fixtures for BlogCraftAI."""
from __future__ import annotations

import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client() -> APIClient:
    client = APIClient()
    return client


@pytest.fixture()
def auth_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(email="author@example.com", password="pass12345")
    api_client.force_authenticate(user=user)
    return api_client, user
