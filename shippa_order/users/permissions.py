from django.shortcuts import get_object_or_404
from rest_framework import permissions

from users.models import User

__all__ = [
    "IsSelf",
    "IsSelfReadOnly"
]


class IsSelf(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        authenticated = super().has_permission(request, view)
        if not authenticated:
            return False

        user_id = view.kwargs['pk']
        user = get_object_or_404(User, pk=user_id)
        return request.user == user and request.method in permissions.SAFE_METHODS


class IsSelfReadOnly(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        authenticated = super().has_permission(request, view)
        if not authenticated:
            return False

        user_id = view.kwargs['pk']
        user = get_object_or_404(User, pk=user_id)
        return request.user == user and request.method in permissions.SAFE_METHODS
