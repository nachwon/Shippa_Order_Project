from django.contrib.auth.models import AbstractUser
from django.db import models

from users import configs


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    points = models.PositiveIntegerField(default=configs.DEFAULT_POINTS)
