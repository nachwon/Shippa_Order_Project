from rest_framework import generics, permissions, status
from rest_framework.response import Response
# Merchant API 1. 주문 -> merchant save.
from order.models import Order, OrderItem
from order.serializers import OrderSerializer, OrderItemSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated, )

    def get(self, request, *args, **kwargs):
        """
        query_params = offset, limit
        """
        user_id = request.user.id
        offset = request.query_params.get('offset', 0)
        limit = request.query_params.get('limit', 10)
        resp = self.get_queryset().filter(user_id=user_id).order_by('created_at')[offset: limit]
        serializer = self.get_serializer_class()
        results = [serializer(r, context={'presentation': 'list'}).data for r in resp]

        return Response({
            'pagination': {
                'offset': offset,
                'limit': limit,
                'total': len(results)
            },
            'results': results
        }, status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        """
        payload: {
            "merchant_id": 1,
            "order_items": [
                {
                    "menu_id": 1, "quantity": 2
                }, ...
            ]
        }
        """
        payload = request.data
        payload['user_id'] = request.user.id
        serializer = self.get_serializer(data=payload)
        is_valid = serializer.is_valid(raise_exception=False)
        if not is_valid:
            return Response(data={'reason': serializer.errors})
        order = serializer.save()
        return Response(data={'order_id': order.id}, status=status.HTTP_201_CREATED)


class OrderRetrieveUpdateDestroyView(generics.RetrieveDestroyAPIView):
    lookup_field = 'id'
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = (permissions.IsAuthenticated,)

    def retrieve(self, request, *args, **kwargs):
        order_object = self.get_object()
        serializer = self.get_serializer_class()
        serializer_data = serializer(order_object, context={'presentation': 'retrieve'}).data

        return Response(data=serializer_data, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        order_object = self.get_object()
        serializer = self.get_serializer(order_object, data={'status': 'CANCELED'}, partial=True)
        serializer.is_valid()
        serializer.save()

        return Response(data={}, status=status.HTTP_204_NO_CONTENT)




