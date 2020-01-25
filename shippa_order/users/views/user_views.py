from rest_framework import generics, permissions

from users.models import User
from users.serializers import UserSerializer
from users import permissions as custom_permissions


__all__ = [
    "UserListView",
    "UserRetrieveUpdateDestroyView"
]


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [custom_permissions.IsSelf | permissions.IsAdminUser]
