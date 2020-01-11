from rest_framework import generics, permissions

from users.models import PointsLog, User
from users.serializers import PointsLogSerializers, PointSerializer
from users import permissions as custom_permissions


__all__ = [
    "PointRetrieveUpdateView",
    "PointsLogListView"
]


class PointRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = PointSerializer
    queryset = User.objects.all()
    permission_classes = [custom_permissions.IsSelfReadOnly | permissions.IsAdminUser]


class PointsLogListView(generics.ListAPIView):
    serializer_class = PointsLogSerializers
    permission_classes = [custom_permissions.IsSelfReadOnly | permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return PointsLog.objects.filter(user__id=user_id)
