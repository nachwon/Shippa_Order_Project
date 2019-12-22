from rest_framework import generics, permissions
from users.models import User
from users.serializers import UserSerializer, PointSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]


class PointRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PointSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
