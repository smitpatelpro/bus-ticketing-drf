# Generated by Django 4.0.6 on 2022-07-21 10:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bus_operator", "0017_alter_busjourney_options"),
    ]

    operations = [
        migrations.RenameField(
            model_name="busjourney",
            old_name="arrival_time",
            new_name="end_time",
        ),
        migrations.RenameField(
            model_name="busjourney",
            old_name="departure_time",
            new_name="start_time",
        ),
    ]