from django.db import models
from common.models import BaseModel
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class BusOperatorProfile(BaseModel):
    APPROVAL_STATUS = (
        ("APPROVED", "APPROVED"),
        ("PENDING_APPROVAL", "PENDING_APPROVAL"),
        ("REJECTED", "REJECTED"),
    )
    user = models.OneToOneField(
        User, related_name="busoperatorprofile_user", on_delete=models.CASCADE
    )
    business_name = models.CharField(max_length=255)
    business_logo = models.ForeignKey(
        "common.Media",
        related_name="busoperatorprofile_business_logos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    office_address = models.TextField()
    ratings = models.IntegerField(null=True, blank=True, default=None, validators=[
            MaxValueValidator(10),
            MinValueValidator(0)
        ])
    approval_status = models.CharField(choices=APPROVAL_STATUS, max_length=20)
    rejection_comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return "{} ({})".format(self.business_name, self.id)
