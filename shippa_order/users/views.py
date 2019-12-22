from rest_framework import generics, permissions
from users.models import User
from users.serializers import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [permissions.IsAdminUser]
