# Generated by Django 3.0.1 on 2019-12-20 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('menu_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='menu.Menu')),
            ],
        ),
    ]
