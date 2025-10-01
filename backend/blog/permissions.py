"""Custom permission classes for blog API endpoints."""
from __future__ import annotations

from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """Allow write access only to the object's author."""

    def has_object_permission(self, request, view, obj) -> bool:  # type: ignore[override]
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "author", None) == request.user


class IsStaffOrReadOnly(permissions.BasePermission):
    """Allow mutation only for staff users."""

    def has_permission(self, request, view):  # type: ignore[override]
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
