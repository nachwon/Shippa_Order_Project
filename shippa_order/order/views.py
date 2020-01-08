from django.shortcuts import render

# Create your views here.

# Merchant API 1. 주문 상태 변경
from rest_framework import generics, permissions

from order.models import Order
from order.serializers import OrderSerializer


class UpdateOrderStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    # used for validating and deserializing input, and for serializing output
    serializer_class = OrderSerializer
    # queryset should be used for returning objects from this view
    queryset = Order.objects.all()

    def get_queryset(self):
        order_id = self.kwargs['order_id']

    def patch(self, request, *args, **kwargs):
        pass


# Merchant API 2. 주문 매출 조회
class OrderSalesReportView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

    def get(self, request, *args, **kwargs):
        pass