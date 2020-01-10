from django.shortcuts import render

# Create your views here.

# Merchant API 1. 주문 상태 변경
from rest_framework import generics, permissions, status
from rest_framework.response import Response

from order.models import Order
from order.serializers import UserOrderSerializer


# 기본적인 Merchant-API RU
# 자기 가게의 주문 총 리스트 조회
class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserOrderSerializer

    def get_queryset(self):
        merchant_id = self.request.query_params.get('merchant_id')
        return Order.objects.filter(merchant_id=merchant_id)

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)
        resp = self.get_queryset().order_by('created_at')[offset: limit]
        serializer = self.get_serializer()

        results = [serializer(r).data for r in resp]

        return Response({
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total': len(results)
            },
            'results': results
        }, status.HTTP_200_OK)


# 특정 주문의 detail view 조회()
class OrderDetailView(generics.RetrieveAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserOrderSerializer
    lookup_field = 'id'
    queryset = Order.objects.all()

    def retrieve(self, request, *args, **kwargs):
        order_object = self.get_object()
        serializer = self.get_serializer(order_object)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


# 주문 상태 변경 API. 결제 취소로 상태 변경시 status 바꾸고 유저 포인트 복구까지. point log 테이블 insert
class UpdateOrderStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.AllowAny]
    # used for validating and deserializing input, and for serializing output
    serializer_class = UserOrderSerializer
    # queryset should be used for returning objects from this view
    queryset = Order.objects.all()

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return Order.objects.filter(id=order_id)

    def patch(self, request, *args, **kwargs):
        order_id = kwargs['order_id']


# Merchant API 2. 주문 매출 조회
class OrderSalesReportView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = UserOrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        # 해당 날짜의 Order list를 가져옴.

    def get(self, request, *args, **kwargs):
        pass
