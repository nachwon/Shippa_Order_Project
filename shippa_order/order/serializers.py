import datetime
from django.db import transaction
from rest_framework import serializers

from merchants.models import Merchant, Menu
from merchants.serializers import MenuSerializer
from order.models import Order, OrderItem
from users.serializers import PointSerializer


class OrderSerializer(serializers.ModelSerializer):
    """
    Self Order List, Order Create
    """
    order_items = serializers.JSONField()

    class Meta:
        model = Order
        fields = ['id', 'status', 'user', 'created_at', 'last_updated_time', 'merchant', 'order_items', 'message', 'total_price']
        read_only_fields = ['id', 'created_at', 'total_price']
        extra_kwargs = {'user': {'write_only': True, 'required': True},
                        'merchant': {'write_only': True, 'required': True},
                        'order_items': {'write_only': True, 'required': True},
                        'message': {'write_only': True}}

    def to_representation(self, instance):
        if instance.merchant is None:
            merchant_name = None
        else:
            merchant_object = Merchant.objects.get(id=instance.merchant.id)
            merchant_name = merchant_object.name
        order_item = OrderItem.objects.filter(order=instance.id)
        order_item_serializer = OrderItemSerializer(order_item, many=True)

        return {
            'id': instance.id,
            'status': instance.status,
            'create_at': datetime.datetime.strftime(instance.created_at, '%Y-%m-%d %H:%M:%S'),
            'last_updated_time': datetime.datetime.strftime(instance.last_updated_time, '%Y-%m-%d %H:%M:%S'),
            'merchant_id': instance.merchant.id if instance.merchant else None,
            'merchant_name': merchant_name,
            'order_items': order_item_serializer.data
        }

    @transaction.atomic()
    def create(self, validated_data):
        # Todo is_available_menus(menu_ids)
        menu_ids = sorted([data['menu_id'] for data in validated_data['order_items']])
        menu_objects = Menu.objects.filter(id__in=menu_ids)
        # Todo get_price_by_menus(menu_ids)
        # Todo calculate total price

        dummy_total_price = sum([menu.price * order_item['quantity']
                                 for menu, order_item in zip(menu_objects, validated_data['order_items'])])
        user = validated_data['user']

        order_object = Order.objects.create(user=validated_data['user'],
                                            message=validated_data.get('message'),
                                            merchant=validated_data['merchant'],
                                            total_price=dummy_total_price)
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order_object,
                menu=menu_object,
                quantity=order_item['quantity'],
                menu_price=menu_object.price,
                total_price=order_item['quantity'] * menu_object.price
            )
            for menu_object, order_item in zip(menu_objects, validated_data['order_items'])])
        user_point_serializer = PointSerializer(user, data={
            'points_spent': dummy_total_price
        }, partial=True)
        user_point_serializer.is_valid()
        user_point_serializer.save()

        return order_object

    @transaction.atomic()
    def update(self, instance, validated_data):
        """
         Order Cancel
        """
        if validated_data.get('status') and instance.status != 'PENDING':
            raise
        instance.status = validated_data['status']
        instance.save()

        points_serializer = PointSerializer(instance.user, data={'points_added': instance.total_price}, partial=True)
        points_serializer.is_valid()
        points_serializer.save()

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()
    total_price = serializers.CharField(max_length=10)

    class Meta:
        model = OrderItem
        fields = ['menu', 'quantity', 'menu_price', 'total_price']
        read_only_fields = ['total_price', 'menu_price']
        depth = 2

    def update(self, instance, validated_data):
        if Order.objects.get(id=instance.order).status != 'PENDING':
            # Todo write detail raise
            raise

        if validated_data.get('quantity'):
            instance.quantity = validated_data['quantity']
        if validated_data.get('menu'):
            instance.menu = validated_data['menu']
        if validated_data.get('menu_price'):
            instance.menu_price = validated_data['menu_price']
            instance.total_price = instance.menu_price * instance.quantity

        instance.save()

        return instance

