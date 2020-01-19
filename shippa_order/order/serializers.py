import datetime
from django.db import transaction
from rest_framework import serializers

from common.exceptions import OrderCanCelFailedException
from merchants.models import Merchant
from merchants.serializers import MenuSerializer
from merchants.utils import MenuManager
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
        presentation_type = self.context.get('presentation')
        if instance.merchant is None:
            merchant_name = None
        else:
            merchant_object = Merchant.objects.get(id=instance.merchant.id)
            merchant_name = merchant_object.name

        return_data = {
                'id': instance.id,
                'status': instance.status,
                'create_at': datetime.datetime.strftime(instance.created_at, '%Y-%m-%d %H:%M:%S'),
                'last_updated_time': datetime.datetime.strftime(instance.last_updated_time, '%Y-%m-%d %H:%M:%S'),
                'merchant_id': instance.merchant.id if instance.merchant else None,
                'merchant_name': merchant_name,
                'total_price': instance.total_price
            }
        if presentation_type == 'retrieve':
            order_item = OrderItem.objects.filter(order=instance.id)
            order_item_serializer = OrderItemSerializer(order_item, many=True)
            return_data['order_items'] = order_item_serializer.data
        return return_data

    @transaction.atomic()
    def create(self, validated_data):
        menu_ids = sorted([data['menu_id'] for data in validated_data['order_items']])
        menu_manager = MenuManager(merchant_id=validated_data['merchant'].id, menu_ids=menu_ids)
        menu_manager.check_if_menus_order_is_available()
        menu_objects = menu_manager.get_menus_for_order()
        total_price = sum([menu_objects[order_item['menu_id']].discounted_price * order_item['quantity']
                           for order_item in validated_data['order_items']])

        user = validated_data['user']

        order_object = Order.objects.create(user=validated_data['user'],
                                            message=validated_data.get('message'),
                                            merchant=validated_data['merchant'],
                                            total_price=total_price)
        menus = {menu.id: menu for menu in menu_manager.menus}
        OrderItem.objects.bulk_create([
            OrderItem(
                order=order_object,
                menu=menus[order_item['menu_id']],
                quantity=order_item['quantity'],
                menu_price=menu_objects[order_item['menu_id']].price,
                total_price=order_item['quantity'] * menu_objects[order_item['menu_id']].discounted_price,
                discounted_price=menu_objects[order_item['menu_id']].discounted_price,
                discount_ratio=menu_objects[order_item['menu_id']].discount_ratio
            ) for order_item in validated_data['order_items']])

        user_point_serializer = PointSerializer(user, data={
            'points_spent': total_price
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
            raise OrderCanCelFailedException(detail='Order cancellation is only possible when the status is pending.')
        instance.status = validated_data['status']
        instance.save()

        points_serializer = PointSerializer(instance.user, data={'points_added': instance.total_price}, partial=True)
        points_serializer.is_valid()
        points_serializer.save()

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    menu = MenuSerializer()

    class Meta:
        model = OrderItem
        fields = ['menu', 'quantity', 'menu_price', 'total_price']
        read_only_fields = ['total_price', 'menu_price']
        depth = 2

    def update(self, instance, validated_data):
        # Supported Not Yet
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

    def to_representation(self, instance):

        return {
            'order_id': instance.id,
            'menu_id': instance.menu.id,
            'quantity': instance.quantity,
            'menu_price': instance.menu_price,
            'total_price': instance.total_price,
            'discounted_price': instance.discounted_price,
            'discount_ratio': instance.discount_ratio
        }

