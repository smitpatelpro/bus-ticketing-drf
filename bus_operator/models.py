from django.db import models
from common.models import BaseModel
from django.contrib.auth import get_user_model

User = get_user_model()


class BusOperatorProfile(BaseModel):
    APPROVAL_STATUS = (
        ("APPROVED", "APPROVED"),
        ("PENDING_APPROVAL", "PENDING_APPROVAL"),
        ("REJECTED", "REJECTED"),
    )
    user = models.OneToOneField(
        User, related_name="opertor_profile", on_delete=models.CASCADE
    )
    business_name = models.CharField(max_length=255)
    business_logo = models.ForeignKey(
        "common.Media",
        related_name="operator_business_logos",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    office_address = models.TextField()
    ratings = models.IntegerField(null=True, blank=True, default=None)
    approval_status = models.CharField(choices=APPROVAL_STATUS, max_length=20)
    rejection_comment = models.TextField(blank=True)

    def __str__(self) -> str:
        return "{} ({})".format(self.business_name, self.id)


class Bus(BaseModel):
    BUS_TYPES = (
        ("REGULAR", "REGULAR"),
        ("SLEEPER", "SLEEPER"),
        ("SLEEPER_DUPLEX", "SLEEPER_DUPLEX"),
    )
    operator = models.ForeignKey(
        "BusOperatorProfile", related_name="buses", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    type = models.CharField(choices=BUS_TYPES, max_length=20)
    capacity = models.IntegerField(default=0)
    per_km_fare = models.DecimalField(max_digits=6, decimal_places=2)
    photos = models.ManyToManyField("common.Media", blank=True)
    amenities = models.ManyToManyField("BusAmenity", blank=True)


class BusAmenity(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()


class BusUnavailability(BaseModel):
    bus = models.ForeignKey(
        "Bus", on_delete=models.CASCADE, related_name="unavailabilities"
    )
    date = models.DateField()
    reason = models.TextField()


class BusStoppage(BaseModel):
    JOURNEY_TYPES = (
        ("UP", "UP"),
        ("DOWN", "DOWN"),
    )
    bus = models.ForeignKey("Bus", on_delete=models.CASCADE, related_name="stoppages")
    name = models.CharField(max_length=255)
    departure_time = models.DateField()
    arrival_time = models.DateField()
    distance = models.IntegerField(default=0)
    journey_type = models.CharField(choices=JOURNEY_TYPES, max_length=20)
