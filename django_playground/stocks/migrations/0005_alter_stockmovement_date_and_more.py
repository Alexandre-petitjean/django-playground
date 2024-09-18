# Generated by Django 5.0.9 on 2024-09-12 12:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stocks', '0004_alter_stockmovement_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stockmovement',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 12, 12, 20, 33, 908000, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='stockmovement',
            name='movement_type',
            field=models.CharField(choices=[('in', 'Incoming'), ('out', 'Outgoing')], default='in', max_length=3),
        ),
    ]