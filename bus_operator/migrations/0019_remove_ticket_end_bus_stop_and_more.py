# Generated by Django 4.0.6 on 2022-07-22 07:41

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_operator', '0018_rename_arrival_time_busjourney_end_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticket',
            name='end_bus_stop',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='start_bus_stop',
        ),
        migrations.AddField(
            model_name='ticket',
            name='journey_end',
            field=models.CharField(default='ahmedabad', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='journey_start',
            field=models.CharField(default='jaipur', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ticket',
            name='seats',
            field=models.IntegerField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
            preserve_default=False,
        ),
    ]
