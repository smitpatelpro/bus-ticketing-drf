# Generated by Django 4.0.6 on 2022-07-20 12:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0001_initial"),
        ("bus_operator", "0014_rename_distance_busstoppage_distance_from_last_stop"),
    ]

    operations = [
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "deleted_at",
                    models.DateTimeField(
                        blank=True,
                        db_index=True,
                        default=None,
                        editable=False,
                        null=True,
                    ),
                ),
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("journey_date", models.DateField()),
                ("number", models.CharField(max_length=255)),
                ("invoice_number", models.CharField(max_length=255)),
                ("transaction_id", models.CharField(max_length=255)),
                (
                    "rating",
                    models.IntegerField(
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(10),
                        ]
                    ),
                ),
                (
                    "payment_status",
                    models.CharField(
                        choices=[
                            ("REGULAR", "REGULAR"),
                            ("SLEEPER", "SLEEPER"),
                            ("SLEEPER_DUPLEX", "SLEEPER_DUPLEX"),
                        ],
                        max_length=20,
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=6,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                (
                    "bus",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_bus",
                        to="bus_operator.bus",
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_customer",
                        to="customer.customerprofile",
                    ),
                ),
                (
                    "end_bus_stop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_end_bus_stop",
                        to="bus_operator.busstoppage",
                    ),
                ),
                (
                    "start_bus_stop",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="ticket_start_bus_stop",
                        to="bus_operator.busstoppage",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
