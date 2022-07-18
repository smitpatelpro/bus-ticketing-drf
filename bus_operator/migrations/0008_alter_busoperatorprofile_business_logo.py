# Generated by Django 4.0.6 on 2022-07-18 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("common", "0003_alter_user_phone_number"),
        ("bus_operator", "0007_merge_20220718_0952"),
    ]

    operations = [
        migrations.AlterField(
            model_name="busoperatorprofile",
            name="business_logo",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="busoperatorprofile_business_logo",
                to="common.media",
            ),
        ),
    ]
