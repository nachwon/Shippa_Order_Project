from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound, ValidationError

from merchants.models import Menu
from merchants.serializers import MenuSerializer
from order.models import Order, OrderItem


class MenuField(serializers.RelatedField):
    queryset = Menu.objects.all()

    def to_representation(self, value):
        return MenuSerializer(value).data

    def to_internal_value(self, data):
        try:
            return Menu.objects.get(pk=data)
        except Menu.DoesNotExist:
            raise NotFound(detail="Menu does not exists.")


class OrderItemSerializer(serializers.ModelSerializer):
    menu = MenuField()

    class Meta:
        model = OrderItem
        fields = (
            "id", "menu", "quantity"
        )

    def validate_menu(self, value):
        merchant_id = self.context.get('merchant_id')

        if value.merchant_id != merchant_id:
            raise ValidationError("Invalid menu. This menu does not belong to this merchant.")

        if value.out_of_stock:
            raise ValidationError(f"{value} is out of stock.")
        return value


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "id", "user", "merchant", "status", "message", "created_at", "updated_at", "order_items", "total_price"
        )

    def create(self, validated_data):
        order_item_data = validated_data.pop('order_items')
        with transaction.atomic():
            order = Order(**validated_data)

            order_item_objs = []
            for order_item in order_item_data:
                order_item_objs.append(OrderItem(order=order, **order_item))

            order.save()

            for item in order_item_objs:
                item.save()

            try:
                order.save_total_price()
            except DjangoValidationError as e:
                raise ValidationError(detail={"error": e.message})

        return order

    def update(self, instance: Order, validated_data):
        with transaction.atomic():
            status = validated_data.get('status', None)
            if status and status == instance.status:
                raise ValidationError(detail={
                    "status": "Cannot update to the same status."
                })

            instance = super().update(instance, validated_data)
            if status and status == Order.OrderStatus.Completed:
                instance.user.spend_points(instance.total_price)
        return instance
