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
        InProgress = 'INPROGRESS', _('InProgress')
        Completed = 'COMPLETED', _('Completed')
        Canceled = 'CANCELED', _('Canceled')
        Failed = 'FAILED', _('Failed')
        Refunded = 'REFUNDED', _('Refunded')

    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    merchant = models.ForeignKey(Merchant, null=True, on_delete=models.PROTECT)
    status = models.CharField(max_length=10, choices=OrderStatus.choices, default=OrderStatus.Pending)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)
    message = models.CharField(max_length=30, null=True)
    total_price = models.PositiveIntegerField()
    objects = models.Manager()


class OrderItem(models.Model):
    class Meta:
        unique_together = [['order_id', 'menu_id']]
        indexes = [
            models.Index(fields=['order_id'])
        ]

    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    menu = models.ForeignKey(Menu, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    menu_price = models.PositiveIntegerField()
    discounted_price = models.PositiveIntegerField(default=0)
    discount_ratio = models.FloatField(default=0.0)
    total_price = models.PositiveIntegerField()
    objects = models.Manager()

    def set_total_price(self, menu_price):
        return menu_price * self.quantity

