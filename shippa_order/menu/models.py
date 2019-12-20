from django.db import models


class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32)
    image = models.ImageField()
    price = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"ID: {self.id} - {self.name}"


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    menu_id = models.ForeignKey(Menu, null=True, on_delete=models.SET_NULL)
    quantity = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order {self.id}"
