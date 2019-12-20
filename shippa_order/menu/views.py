from rest_framework import generics, permissions

from menu.models import Menu
from menu.serializers import MenuSerializer


class MenuListCreateView(generics.ListCreateAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [permissions.AllowAny]


class MenuRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    permission_classes = [permissions.AllowAny]
