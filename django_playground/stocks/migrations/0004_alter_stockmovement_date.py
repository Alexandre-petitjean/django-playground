# Generated by Django 5.0.9 on 2024-09-12 12:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0003_alter_product_quantity_in_stock'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 12, 12, 12, 30, 237221, tzinfo=datetime.timezone.utc)),
        ),
    ]
