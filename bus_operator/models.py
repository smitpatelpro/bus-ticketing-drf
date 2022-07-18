from django.db import models
from common.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
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
        related_name="busoperatorprofile_business_logo",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    office_address = models.TextField()
    ratings = models.IntegerField(
        null=True,
        blank=True,
        default=None,
        validators=[MaxValueValidator(10), MinValueValidator(0)],
    )
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
        "BusOperatorProfile", related_name="bus_operator", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=255)
    type = models.CharField(choices=BUS_TYPES, max_length=20)
    capacity = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    per_km_fare = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
    photos = models.ManyToManyField("common.Media", blank=True)
    amenities = models.ManyToManyField("BusAmenity", blank=True)


class BusAmenity(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()


class BusUnavailability(BaseModel):
    bus = models.ForeignKey(
        "Bus", on_delete=models.CASCADE, related_name="busunavailability_bus"
    )
    date = models.DateField()
    reason = models.TextField()

    class Meta:
        unique_together = (
            "bus",
            "date",
        )


class BusStoppage(BaseModel):
    JOURNEY_TYPES = (
        ("UP", "UP"),
        ("DOWN", "DOWN"),
    )
    bus = models.ForeignKey(
        "Bus", on_delete=models.CASCADE, related_name="busstoppage_bus"
    )
    count = models.IntegerField(validators=[MinValueValidator(0)])
    name = models.CharField(max_length=255)
    arrival_time = models.DateField()
    departure_time = models.DateField()
    distance = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )
    journey_type = models.CharField(choices=JOURNEY_TYPES, max_length=20)

    class Meta:
        verbose_name = "Bus Stop"
        verbose_name_plural = "Bus Stops"

    def clean(self) -> None:
        if self.departure_time < self.arrival_time:
            raise ValidationError(
                {
                    "departure_time": "Departure time must be greater or equal to arrival time."
                }
            )
