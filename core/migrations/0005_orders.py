# Generated by Django 5.1.4 on 2024-12-12 16:22

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_products_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('full_name', models.CharField(max_length=100)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.RegexValidator(message='شماره خودرا با فرمت صحیح وارد کنید, با 09 شروع شود و شامل 11 رقم باشد', regex='^09\\d{9}$')])),
                ('city', models.CharField(max_length=50)),
                ('shipping_address', models.CharField(max_length=1500)),
                ('postal_code', models.CharField(max_length=100)),
                ('amount_paid', models.DecimalField(decimal_places=0, max_digits=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('delivered', 'delivered'), ('canceled', 'canceled')], default='pending', max_length=50)),
                ('shipped', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'db_table': 'orders',
                'ordering': ['-created_at'],
                'get_latest_by': 'created_at',
            },
        ),
    ]
