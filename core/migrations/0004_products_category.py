# Generated by Django 5.1.4 on 2024-12-12 15:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_categories'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='category',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='core.categories'),
            preserve_default=False,
        ),
    ]
