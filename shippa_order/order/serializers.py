import datetime

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from rest_framework import serializers

from merchants.models import Merchant, Menu
from merchants.serializers import MenuSerializer
from order.exceptions import ObjectDoesNotExists
from order.models import Order, OrderItem


class UserOrderSerializer(serializers.ModelSerializer):
    """
    Self Order List, Order Create
    """
    order_items = serializers.JSONField()

    class Meta:
        model = Order
        fields = ['id', 'status', 'user_id', 'created_at', 'last_updated_time', 'merchant_id', 'order_items', 'message']
        read_only_fields = ['id', 'created_at']
        extra_kwargs = {'user_id': {'write_only': True, 'required': True},
                        'merchant_id': {'write_only': True, 'required': True},
                        'order_items': {'write_only': True, 'required': True},
                        'message': {'write_only': True}}

    def to_representation(self, instance):
        if instance.merchant_id is None:
            merchant_name = None
        else:
            merchant_object = Merchant.objects.get(id=instance.merchant_id.id)
            merchant_name = merchant_object.name
        order_item = OrderItem.objects.filter(order_id=instance.id)
        order_item_serializer = OrderItemSerializer(order_item, many=True)

        return {
            'id': instance.id,
            'status': instance.status,
            'create_at': datetime.datetime.strftime(instance.created_at, '%Y-%m-%d %H:%M:%S'),
            'last_updated_time': datetime.datetime.strftime(instance.last_updated_time, '%Y-%m-%d %H:%M:%S'),
            'merchant_id': instance.merchant_id.id if instance.merchant_id else None,
            'merchant_name': merchant_name,
            'order_items': order_item_serializer.data
        }

    def validate_order_items(self, value: list):
        try:
            validate_value = [{'menu_id': Menu.objects.get(id=data['menu_id']), 'quantity': data['quantity']}
                              for data in value]
        except ObjectDoesNotExist:
            raise ObjectDoesNotExists('?')

        return validate_value

    @transaction.atomic()
    def create(self, validated_data):
        order_object = Order.objects.create(user_id=validated_data['user_id'],
                                            message=validated_data.get('message'),
                                            merchant_id=validated_data['merchant_id'])
        OrderItem.objects.bulk_create([
            OrderItem(order_id=order_object, menu_id=data['menu_id'], quantity=data['quantity'])
            for data in validated_data['order_items']])

        return order_object

    def update(self, instance, validated_data):
        if instance.status != 'PENDING':
            # Todo Custom Exception
            raise Exception
        instance.status = validated_data['status']
        instance.save()

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    menu_id = MenuSerializer()

    class Meta:
        model = OrderItem
        fields = ['menu_id', 'quantity']
        depth = 2

    def update(self, instance, validated_data):
        if Order.objects.get(id=instance.order_id).status != 'PENDING':
            # Todo write detail raise
            raise
        if validated_data.get('quantity'):
            instance.quantity = validated_data['quantity']
        if validated_data.get('menu_id'):
            instance.menu_id = validated_data['menu_id']
        instance.save()

        return instance

