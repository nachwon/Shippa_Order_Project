from django.shortcuts import render

# Create your views here.

# Merchant API 1. 주문 상태 변경
from rest_framework import generics, permissions

from order.serializers import OrderSerializer


class UpdateOrderStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def get_queryset(self):
        pass

    def patch(self):
        pass


# Merchant API 2. 주문 매출 조회
class OrderSalesReportView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer

    def get_queryset(self):
        pass

    def get(self):
        pass