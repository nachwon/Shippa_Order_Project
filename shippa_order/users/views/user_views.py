from rest_framework import generics, permissions

from users.models import User
from users.serializers import UserSerializer, PointSerializer
from users import permissions as custom_permissions


__all__ = [
    "UserListView",
    "UserRetrieveUpdateDestroyView",
    "PointRetrieveUpdateView"
]


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [custom_permissions.IsSelf | permissions.IsAdminUser]


class PointRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PointSerializer
    queryset = User.objects.all()
    permission_classes = [custom_permissions.IsSelfReadOnly | permissions.IsAdminUser]
