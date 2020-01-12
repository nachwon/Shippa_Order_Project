from django.db import models


class Merchant(models.Model):
    # base
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=24, unique=True)

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


class Menu(models.Model):
    # base
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=128)
    image = models.CharField(max_length=128, null=True)
    price = models.PositiveSmallIntegerField()
    currency = models.CharField(max_length=3)
    quantity = models.SmallIntegerField(default=0)

    merchant = models.ForeignKey(Merchant, on_delete=models.CASCADE)

    # option
    closed = models.BooleanField(default=True)

    # date
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    class Meta:
        order_with_respect_to = 'merchant'
        indexes = [
            models.Index(fields=['merchant_id', ]),
            models.Index(fields=['merchant_id', 'closed', ]),
        ]
