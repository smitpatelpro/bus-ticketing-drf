# Generated by Django 4.0.6 on 2022-07-20 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bus_operator", "0013_alter_busstoppage_options_alter_busstoppage_count"),
    ]

    operations = [
        migrations.RenameField(
            model_name="busstoppage",
            old_name="distance",
            new_name="distance_from_last_stop",
        ),
    ]
