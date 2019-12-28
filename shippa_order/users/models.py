import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users import configs


class User(AbstractUser):
    id = models.CharField(max_length=32, primary_key=True, default=uuid.uuid4().hex)
    points = models.PositiveIntegerField(default=configs.DEFAULT_POINTS)


class PointsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points_spent = models.PositiveIntegerField(default=0)
    points_added = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        operator = "+" if self.points_added else "-"
        points = self.points_added or self.points_spent
        return f"{self.user.username} {operator} {points}"
