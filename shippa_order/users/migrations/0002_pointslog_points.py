# Generated by Django 3.0.1 on 2020-01-24 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pointslog',
            name='points',
            field=models.PositiveIntegerField(default=0),
        ),
    ]