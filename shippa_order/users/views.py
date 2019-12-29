from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.serializers import UserSerializer, PointSerializer, CustomTokenObtainPairSerializer


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


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
