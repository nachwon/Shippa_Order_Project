from rest_framework import generics, permissions

from users.models import PointsLog
from users.serializers import PointsLogSerializers
from users import permissions as custom_permissions


__all__ = [
    "PointsLogListView"
]


class PointsLogListView(generics.ListAPIView):
    serializer_class = PointsLogSerializers
    permission_classes = [custom_permissions.IsSelfReadOnly | permissions.IsAdminUser]

    def get_queryset(self):
        user_id = self.kwargs['pk']
        return PointsLog.objects.filter(user__id=user_id)
