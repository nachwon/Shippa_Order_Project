# Generated by Django 3.0.1 on 2019-12-20 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
