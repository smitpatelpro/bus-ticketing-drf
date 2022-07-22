# Generated by Django 4.0.6 on 2022-07-22 08:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus_operator', '0021_ticket_payment_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='invoice_number',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'PENDING'), ('SUCCESSFUL', 'SUCCESSFUL'), ('FAILED', 'FAILED')], max_length=20),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='rating',
            field=models.IntegerField(blank=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(10)]),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='transaction_id',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]