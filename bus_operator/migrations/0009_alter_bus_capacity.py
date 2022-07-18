# Generated by Django 4.0.6 on 2022-07-18 10:45

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bus_operator", "0008_alter_busoperatorprofile_business_logo"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bus",
            name="capacity",
            field=models.IntegerField(
                validators=[
                    django.core.validators.MinValueValidator(0),
                    django.core.validators.MaxValueValidator(100),
                ]
            ),
        ),
    ]
