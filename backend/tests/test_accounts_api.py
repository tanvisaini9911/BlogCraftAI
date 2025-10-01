from __future__ import annotations

import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from .factories import UserFactory

User = get_user_model()


@pytest.mark.django_db
def test_register_creates_user(api_client):
    payload = {
        "email": "learner@example.com",
        "password": "Supersafe123!",
        "display_name": "Learner",
    }
    response = api_client.post("/accounts/register/", payload, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(email=payload["email"]).exists()


@pytest.mark.django_db
def test_register_requires_password(api_client):
    payload = {"email": "nopass@example.com"}
    response = api_client.post("/accounts/register/", payload, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_jwt_token_flow(api_client):
    user = UserFactory(password="Complex123!")
    response = api_client.post(
        "/accounts/token/",
        {"email": user.email, "password": "Complex123!"},
        format="json",
    )
    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_profile_update(auth_client):
    client, user = auth_client
    response = client.patch("/accounts/profile/", {"display_name": "Updated"}, format="json")
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.display_name == "Updated"


@pytest.mark.django_db
def test_password_change_validation(auth_client):
    client, user = auth_client
    response = client.put(
        "/accounts/password-change/",
        {"old_password": "wrong", "new_password": "Newpass123!"},
        format="json",
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
