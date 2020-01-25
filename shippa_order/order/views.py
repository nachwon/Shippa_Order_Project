from rest_framework import generics, permissions
from rest_framework.response import Response

from order.models import Order
from order.serializers import OrderSerializer
from users import permissions as user_permissions


class MerchantOrderListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def get_queryset(self):
        merchant_id = self.kwargs.get('merchant_id')
        return Order.objects.filter(merchant_id=merchant_id)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer_class()
        data = {
            "merchant": self.kwargs.get('merchant_id'),
            **request.data
        }
        serialized_order = serializer(data=data, context=self.kwargs)

        if serialized_order.is_valid():
            serialized_order.save()
            return Response(serialized_order.data)
        else:
            return Response(serialized_order.errors)


class MerchantOrderRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        merchant_id = self.kwargs.get('merchant_id')
        order_id = self.kwargs.get('order_id')
        return Order.objects.filter(merchant_id=merchant_id).filter(pk=order_id)


class UserOrderListView(generics.ListAPIView):
    permission_classes = [user_permissions.IsSelf]
    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        return Order.objects.filter(user_id=user_id)


class UserOrderDetailView(generics.RetrieveAPIView):
    permission_classes = [user_permissions.IsSelf]
    serializer_class = OrderSerializer
    lookup_url_kwarg = 'order_id'

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        order_id = self.kwargs.get('order_id')
        return Order.objects.filter(user_id=user_id).filter(pk=order_id)
