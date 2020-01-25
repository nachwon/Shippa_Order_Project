from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models, transaction

from users import configs


class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    points = models.PositiveIntegerField(default=configs.DEFAULT_POINTS)

    def spend_points(self, points):
        if not points:
            return
        if self.points < points:
            raise ValidationError(message="Not enough points left.")
        self.points -= points

        with transaction.atomic():
            self.save()
            PointsLog.objects.create(
                user=self,
                points_spent=points,
                points=self.points
            ).save()

    def add_points(self, points):
        if not points:
            return

        self.points += points
        with transaction.atomic():
            self.save()
            PointsLog.objects.create(
                user=self,
                points_added=points,
                points=self.points
            ).save()


class PointsLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    points_spent = models.PositiveIntegerField(default=0)
    points_added = models.PositiveIntegerField(default=0)
    points = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        operator = "+" if self.points_added else "-"
        points = self.points_added or self.points_spent
        return f"{self.user.username} {operator} {points}"
