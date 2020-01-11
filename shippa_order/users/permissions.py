from rest_framework.permissions import SAFE_METHODS, IsAdminUser

__all__ = [
    "IsAdminOrSelf",
    "IsSelfReadOnlyOrAdmin"
]


class IsAdminOrSelf(IsAdminUser):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        is_admin = super().has_permission(request, view)
        if is_admin or request.user == view.get_object():
            return True


class IsSelfReadOnlyOrAdmin(IsAdminUser):
    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        is_admin = super().has_permission(request, view)
        if is_admin:
            return True

        if request.user == view.get_object() and request.method in SAFE_METHODS:
            return True
