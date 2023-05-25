from django.db import models
from django.contrib.auth import get_user_model
from common.models import BaseModel

User = get_user_model()


class CustomerProfile(BaseModel):
    GENDER = (
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
        ("BISEXUAL", "BISEXUAL"),
    )
    user = models.OneToOneField(
        User, related_name="customerprofile_user", on_delete=models.CASCADE
    )
    gender = models.CharField(choices=GENDER, max_length=10)
    address = models.TextField()
    id_proof = models.ForeignKey(
        "common.Media",
        related_name="customerprofile_idproof",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    address_proof = models.ForeignKey(
        "common.Media",
        related_name="customerprofile_addressproof",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    other_kyc_document = models.ForeignKey(
        "common.Media",
        related_name="customerprofile_otherkycdocument",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return "{} ({})".format(self.user.full_name, self.id)
