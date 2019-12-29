from rest_framework import generics, permissions
from django.db.models import Q

from merchants.models import Merchant, Menu
from merchants.serializers import MerchantSerializer, MenuSerializer


class MerchantListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MerchantSerializer
    queryset = Merchant.objects.all()


class MerchantRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MerchantSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Merchant.objects.filter(pk=pk)


class MenuListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuSerializer

    def get_queryset(self):
        merchant_id = self.kwargs['merchant_id']
        return Menu.objects.filter(merchant=merchant_id)

    def get_serializer_context(self):
        return {'merchant_id': self.kwargs['merchant_id']}


class MenuRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = MenuSerializer

    def get_queryset(self):
        merchant_id = self.kwargs['merchant_id']
        pk = self.kwargs['pk']
        return Menu.objects.filter(Q(merchant=merchant_id) & Q(pk=pk))

    def get_serializer_context(self):
        return {'merchant_id': self.kwargs['merchant_id']}
