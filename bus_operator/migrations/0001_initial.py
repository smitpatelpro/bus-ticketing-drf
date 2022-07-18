# Generated by Django 4.0.6 on 2022-07-14 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("common", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BusOperatorProfile",
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
                ("business_name", models.CharField(max_length=255)),
                ("office_address", models.TextField()),
                ("ratings", models.IntegerField(blank=True, default=None, null=True)),
                (
                    "approval_status",
                    models.CharField(
                        choices=[
                            ("APPROVED", "APPROVED"),
                            ("PENDING_APPROVAL", "PENDING_APPROVAL"),
                            ("REJECTED", "REJECTED"),
                        ],
                        max_length=20,
                    ),
                ),
                ("rejection_comment", models.TextField(blank=True)),
                (
                    "business_logo",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="operator_business_logos",
                        to="common.media",
                    ),
                ),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="opertor_profile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]