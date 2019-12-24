from django.db import models


class Merchant(models.Model):
    # base
    id = models.UUIDField(primary_key=True)
    name = models.CharField(max_length=128)
    email = models.EmailField(max_length=128, unique=True)
    phone = models.CharField(max_length=24, unique=True)

    # operating time
    forced_closing = models.BooleanField(default=True)

    # 1000000: SUN
    # 0100000: MON
    # 0 ~ 127(every day)
    # ex> 1010101 AND 0000001(SAT) => 0000001 open!
    # ex> 1010101 AND 0000010(FRI) => 0000000 close!
    business_day = models.PositiveSmallIntegerField(null=True)

    open_time = models.TimeField(null=True)
    close_time = models.TimeField(null=True)

    # location
    country_iso = models.CharField(max_length=2)
    city = models.CharField(max_length=64)
    detail_address = models.CharField(max_length=128)

    # date
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    indexes = [
        models.Index(fields=['name', ]),
        models.Index(fields=['email', ]),
        models.Index(fields=['phone', ]),
    ]
