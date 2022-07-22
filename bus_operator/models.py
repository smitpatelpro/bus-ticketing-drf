from django.db import models
from common.models import BaseModel
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import Sum

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

    def get_distance(self, start, end):
        start = self.busjourney_bus.filter(from_place=start).first()
        end = self.busjourney_bus.filter(to_place=end).first()
        if not start or not end:
            return False
        dist = self.busjourney_bus.filter(sequence__gte=start.sequence, sequence__lte=end.sequence).values("distance").aggregate(total_distance=Sum("distance"))
        return int(dist['total_distance'])
    
    def calculate_amount(self, distance):
        return distance * self.per_km_fare
    
    def get_available_capacity(self, start, end):
        start = start.capitalize()
        end = end.capitalize()
        start = self.busjourney_bus.filter(from_place=start).first()
        end = self.busjourney_bus.filter(to_place=end).first()
        if not start or not end:
            return False
        print("start seq: ",start.sequence)
        print("end seq: ",end.sequence)
        previous_places = self.busjourney_bus.filter(sequence__lt=start.sequence).values_list("from_place", flat=True)
        next_places = self.busjourney_bus.filter(sequence__gt=end.sequence).values_list("from_place", flat=True)
        print("previous_places:",previous_places)
        print("next_places:",next_places)
        # dist = self.busjourney_bus.filter(sequence__gte=start.sequence, sequence__lte=end.sequence)
        seats = Ticket.objects.filter(bus=self, payment_status="SUCCESSFUL").exclude(journey_start__in=next_places).exclude(journey_end__in=previous_places)
        print(seats.values("journey_start", "journey_end"))
        seats = seats.aggregate(total_booked_seats=Sum("seats"))
        return self.capacity - int(seats["total_booked_seats"]) if seats["total_booked_seats"] else None


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
    count = models.IntegerField(validators=[MinValueValidator(1)])
    name = models.CharField(max_length=255)
    arrival_time = models.TimeField()
    departure_time = models.TimeField()
    distance_from_last_stop = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )  # Its distance from last stop
    journey_type = models.CharField(choices=JOURNEY_TYPES, max_length=20)

    class Meta:
        verbose_name = "Bus Stop"
        verbose_name_plural = "Bus Stops"
        unique_together = (
            "bus",
            "count",
        )
        ordering = ["bus", "count", "journey_type"]

    def clean(self) -> None:
        if self.departure_time < self.arrival_time:
            raise ValidationError(
                {
                    "departure_time": "Departure time must be greater or equal to arrival time."
                }
            )


class BusJourney(BaseModel):
    JOURNEY_TYPES = (
        ("UP", "UP"),
        ("DOWN", "DOWN"),
    )
    bus = models.ForeignKey(
        "Bus", on_delete=models.CASCADE, related_name="busjourney_bus"
    )
    sequence = models.IntegerField(validators=[MinValueValidator(1)])
    from_place = models.CharField(max_length=255)
    to_place = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    distance = models.IntegerField(
        default=0, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )  # Its distance from last stop
    journey_type = models.CharField(choices=JOURNEY_TYPES, max_length=20)

    class Meta:
        unique_together = (
            "bus",
            "sequence",
            "from_place",
            "to_place",
        )
        ordering = ["sequence"]

    def clean(self) -> None:
        if self.start_time > self.end_time:
            raise ValidationError(
                {"start_time": "Start time must be less then arrival time."}
            )


class Ticket(BaseModel):
    PAYMENT_STATUS = (
        ("PENDING", "PENDING"),
        ("SUCCESSFUL", "SUCCESSFUL"),
        ("FAILED", "FAILED"),
    )

    customer = models.ForeignKey(
        "customer.CustomerProfile",
        related_name="ticket_customer",
        on_delete=models.CASCADE,
    )
    bus = models.ForeignKey("Bus", on_delete=models.CASCADE, related_name="ticket_bus")
    journey_date = models.DateField()
    # start_bus_stop = models.ForeignKey(
    #     "BusStoppage", on_delete=models.CASCADE, related_name="ticket_start_bus_stop"
    # )
    # end_bus_stop = models.ForeignKey(
    #     "BusStoppage", on_delete=models.CASCADE, related_name="ticket_end_bus_stop"
    # )
    
    journey_start = models.CharField(max_length=255)
    journey_end = models.CharField(max_length=255)
    number = models.CharField(max_length=255)
    seats = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    invoice_number = models.CharField(max_length=255, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    rating = models.IntegerField(blank=True, null=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )
    payment_status = models.CharField(choices=PAYMENT_STATUS, max_length=20)
    payment_link = models.URLField(blank=True)
    amount = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(0)]
    )
