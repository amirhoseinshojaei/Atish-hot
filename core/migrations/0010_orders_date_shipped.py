# Generated by Django 5.1.4 on 2024-12-12 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_products_supplier'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='date_shipped',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
