from django.shortcuts import render

# Create your views here.

# Merchant API 1. 주문 상태 변경
from datetime import date
from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from order import exceptions
from order.models import Order
from order.serializers import OrderSerializer


# 기본적인 Merchant-API RU
# 자기 가게의 주문 총 리스트 조회
class MerchantOrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get(self, request, *args, **kwargs):
        limit = request.query_params.get('limit', 10)
        offset = request.query_params.get('offset', 0)
        order_objects = self.get_queryset().filter(merchant=self.kwargs['merchant_id'])[offset: limit]
        results = [self.serializer_class(r).data for r in order_objects]

        return Response({
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total': len(results)
            },
            'results': results
        }, status.HTTP_200_OK)


# 특정 주문의 detail view 조회()
class MerchantOrderRetrieveDestroy(generics.RetrieveDestroyAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    lookup_field = 'merchant_id'
    queryset = Order.objects.all()

    def get_object(self):
        obj = self.get_queryset().get(id=self.kwargs['order_id'])

        self.check_object_permissions(self.request, obj)
        return obj

    def check_object_permissions(self, request, obj):
        # merchant user check가 필요
        if obj.merchant.id != self.kwargs['merchant_id']:
            raise PermissionDenied

    def retrieve(self, request, *args, **kwargs):
        order_object = self.get_object()
        serializer = self.get_serializer(order_object)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        """
        change order status change to CANCELED when status is PENDING
        """
        obj = self.get_object()

        serializer = self.get_serializer(obj, data={'status': 'CANCELED'}, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)


# 주문 상태 변경 API. 결제 취소로 상태 변경시 status 바꾸고 유저 포인트 복구까지. point log 테이블 insert는 자동으로 처리됨.
class MerchantUpdateOrderStatusView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    # used for validating and deserializing input, and for serializing output
    serializer_class = OrderSerializer
    # queryset should be used for returning objects from this view
    queryset = Order.objects.all()

    def get_queryset(self):
        order_id = self.kwargs['order_id']
        return Order.objects.filter(id=order_id)

    def patch(self, request, *args, **kwargs):
        status = request.data.get("status")
        data = self.get_queryset()
        self.serializer_class.update(data, status)

        return Response(data=None, status=status.HTTP_200_OK)


# Merchant API 2. 주문 매출 조회
# 필요한 파라미터 : 년, 월, 일 데이터, merchant_id
# 모델 가져올때 체크사항 : Order의 status 상태가 결제완료 상태인 행만 가져올 것.
class MerchantOrderSalesReportView(generics.ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        merchant_id = self.kwargs['merchant_id']
        year = self.request.query_params.get('year')
        month = self.request.query_params.get('month')
        day = self.request.query_params.get('day')

        if not year or not month or not day:
            raise exceptions.InvalidParameter('year, month, day should be delivered.')

        try:
            parsed_date = date(int(year), int(month), int(day))
        except (ValueError, TypeError):
            raise exceptions.InvalidParameter('year, month, day should be valid date number type.')

        if date.today() < parsed_date:
            raise exceptions.InvalidParameter('requested date should not be post-dated than today.')

        return Order.objects.filter(
            created_at__year=parsed_date.year,
            created_at__month=parsed_date.month,
            created_at__day=parsed_date.day,
            status=Order.OrderStatus.Completed
        )

    def get(self, request, *args, **kwargs):
        items = self.get_queryset()
        total_price = 0
        for item in items:
            total_price += item.total_price

        return Response(data={'total_price': total_price}, status=status.HTTP_200_OK)