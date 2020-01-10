from django.db import models
from django.utils.translation import gettext_lazy as _

from merchants.models import Merchant, Menu
from users.models import User


class Order(models.Model):
    class Meta:
        unique_together = [['id', 'user_id']]
        indexes = [
            models.Index(fields=['user_id'])
        ]

    class OrderStatus(models.TextChoices):
        Pending = 'PENDING', _('Pending')
        Completed = 'COMPLETED', _('Completed')
        Canceled = 'CANCELED', _('Canceled')
        Failed = 'FAILED', _('Failed')
        Refunded = 'REFUNDED', _('Refunded')

    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.Pending)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=30, null=True)
    merchant_id = models.ForeignKey(Merchant, null=True, on_delete=models.PROTECT)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)


class OrderItem(models.Model):
    class Meta:
        unique_together = [['order_id', 'menu_id']]
        indexes = [
            models.Index(fields=['order_id'])
        ]

    order_id = models.ForeignKey(Order, on_delete=models.PROTECT)
    menu_id = models.ForeignKey(Menu, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    menu_price = models.DecimalField(max_digits=12, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2)

    def set_total_price(self, menu_price):
        return menu_price * self.quantity

