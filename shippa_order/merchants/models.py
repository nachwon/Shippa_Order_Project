from django.db import models

from users.models import User


class Merchant(models.Model):
    # base
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=24, unique=True)

    # admin user
    admin_users = models.ManyToManyField(User)

    # operating time
    forced_closing = models.BooleanField(default=True)

    # 0000001: SUN
    # 0000010: MON
    # 0 ~ 127(every day)
    # ex> 1010101 AND 1000000(SAT) => 1000000 open!
    # ex> 1010101 AND 0100000(FRI) => 0000000 close!
    business_days = models.PositiveSmallIntegerField(default=0)
    open_time = models.TimeField(default='00:00:00')
    close_time = models.TimeField(default='00:00:00')

    # location
    country_iso = models.CharField(max_length=2)
    city = models.CharField(max_length=64)
    detail_address = models.CharField(max_length=128)

    # date
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['name', ]),
            models.Index(fields=['email', ]),
            models.Index(fields=['phone', ]),
        ]

    def __str__(self):
        return self.name


class Menu(models.Model):
    # base
    id = models.AutoField(primary_key=True, editable=False)
    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    image = models.CharField(max_length=128, null=True)
    original_price = models.PositiveSmallIntegerField(default=0)
    discount = models.PositiveSmallIntegerField(default=0)

    # option
    out_of_stock = models.BooleanField(default=False)

    # date
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'merchant'
        indexes = [
            models.Index(fields=['merchant_id', ]),
            models.Index(fields=['merchant_id', 'out_of_stock', ]),
        ]

    def __str__(self):
        return f"{self.merchant}: {self.name} - {self.price}"
    
    @property
    def price(self):
        return self.original_price - self.discount
