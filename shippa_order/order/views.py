from django.shortcuts import render

# Create your views here.

# Merchant API 1. 주문 상태 변경
from rest_framework import generics, permissions

from order.models import Order
from order.serializers import OrderSerializer


# 기본적인 Merchant-API RUD
# 자기 가게의 주문 총 리스트 조회
# 특정 주문의 detail view 조회()
# 결제 취소 API -> status 바꾸고 유저 포인트 복구까지. point log 테이블 insert
class UpdateOrderStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    # used for validating and deserializing input, and for serializing output
    serializer_class = OrderSerializer
    # queryset should be used for returning objects from this view
    queryset = Order.objects.all()

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return Order.objects.filter(id=order_id)

    def patch(self, request, *args, **kwargs):
        order_id = kwargs['order_id']

# Merchant API 2. 주문 매출 조회
class OrderSalesReportView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        # 해당 날짜의 Order list를 가져옴.

    def get(self, request, *args, **kwargs):
        pass
