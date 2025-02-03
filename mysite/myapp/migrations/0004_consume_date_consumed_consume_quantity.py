# Generated by Django 5.1.5 on 2025-01-29 21:01

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_rename_cosume_consume'),
    ]

    operations = [
        migrations.AddField(
            model_name='consume',
            name='date_consumed',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='consume',
            name='quantity',
            field=models.FloatField(default=1),
        ),
    ]
