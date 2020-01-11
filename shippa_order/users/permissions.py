from rest_framework import permissions

__all__ = [
    "IsSelf",
    "IsSelfReadOnly"
]


class IsSelf(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        print(request.user == obj, request.user.is_staff)
        return request.user == obj


class IsSelfReadOnly(permissions.IsAuthenticated):

    def has_object_permission(self, request, view, obj):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if request.user == obj and request.method in permissions.SAFE_METHODS:
            return True
