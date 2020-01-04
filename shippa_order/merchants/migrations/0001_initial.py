# Generated by Django 3.0.1 on 2020-01-04 10:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('image', models.CharField(max_length=128, null=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=12)),
                ('currency', models.CharField(max_length=3)),
                ('quantity', models.SmallIntegerField(default=0)),
                ('closed', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=128)),
                ('email', models.EmailField(max_length=128, unique=True)),
                ('phone', models.CharField(max_length=24, unique=True)),
                ('forced_closing', models.BooleanField(default=True)),
                ('business_days', models.PositiveSmallIntegerField(default=0)),
                ('open_time', models.TimeField(default='00:00:00')),
                ('close_time', models.TimeField(default='00:00:00')),
                ('country_iso', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=64)),
                ('detail_address', models.CharField(max_length=128)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('last_updated_time', models.DateTimeField(auto_now=True)),
            ],
        ),

        migrations.AddIndex(
            model_name='merchant',
            index=models.Index(fields=['name'], name='merchants_m_name_bfa087_idx'),
        ),
        migrations.AddIndex(
            model_name='merchant',
            index=models.Index(fields=['email'], name='merchants_m_email_dab763_idx'),
        ),
        migrations.AddIndex(
            model_name='merchant',
            index=models.Index(fields=['phone'], name='merchants_m_phone_00a594_idx'),
        ),
        migrations.AddField(
            model_name='menu',
            name='merchant',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchants.Merchant'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['merchant_id'], name='merchants_m_merchan_7655b7_idx'),
        ),
        migrations.AddIndex(
            model_name='menu',
            index=models.Index(fields=['merchant_id', 'closed'], name='merchants_m_merchan_939bc8_idx'),
        ),
        migrations.AlterOrderWithRespectTo(
            name='menu',
            order_with_respect_to='merchant',
        ),
    ]
