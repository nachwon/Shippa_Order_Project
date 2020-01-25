from collections import OrderedDict

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from merchants.models import Merchant, Menu
from users.models import User


class Order(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['user_id'])
        ]

    class OrderStatus(models.TextChoices):
        Pending = 'PENDING', _('Pending')              # Order placed but menu not yet ready
        Ready = 'READY', _('Ready')                    # Menu is ready and waiting for the user.
        Completed = 'COMPLETED', _('Completed')        # User took the menu and paid the price.
        Canceled = 'CANCELED', _('Canceled')           # Order have been canceled before complete.
        Failed = 'FAILED', _('Failed')                 # Process have failed due to unexpected reasons.
        Refunded = 'REFUNDED', _('Refunded')

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    merchant = models.ForeignKey(Merchant, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.Pending)
    message = models.CharField(max_length=30, null=True, blank=True)
    total_price = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.merchant.name} - {self.user.username}:{self.status}"

    @staticmethod
    def calculate_total_price(order_items):
        total_price = 0
        for item in order_items:
            if isinstance(item, OrderItem):
                total_price += item.menu.price * item.quantity
            elif isinstance(item, OrderedDict):
                total_price += item.get('menu').price * item.get('quantity')
        return total_price

    def validate_total_price(self):
        if self.user.points < self.total_price:
            raise ValidationError(f"{self.user.username} does not have enough points to place this order.")

    def save_total_price(self):
        order_items = self.order_items.all()
        self.total_price = self.calculate_total_price(order_items)
        self.validate_total_price()
        self.save()


class OrderItem(models.Model):
    class Meta:
        indexes = [
            models.Index(fields=['order_id'])
        ]

    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.menu.name} - {self.quantity}"
