from django.contrib import admin
from . import models

# Inlines
class BusStoppageInline(admin.TabularInline):
    model = models.BusStoppage
    ordering = ["count"]


# Inlines
class BusJourneyInline(admin.TabularInline):
    model = models.BusJourney
    ordering = ["sequence"]


# Model Admin
@admin.register(models.BusOperatorProfile)
class BusOperatorProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "operator", "capacity")
    inlines = [
        BusStoppageInline,
        BusJourneyInline,
    ]
    pass


@admin.register(models.BusAmenity)
class BusAmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStoppage)
class BusStoppageAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "bus_name",
        "count",
        "name",
        "arrival_time",
        "departure_time",
        "distance_from_last_stop",
        "journey_type",
    )

    def bus_name(self, object):
        return "{} ({})".format(object.bus.name, object.bus.id)


@admin.register(models.BusUnavailability)
class BusUnavailabilityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "number",
        "customer",
        "bus",
        "journey_date",
        # "journey_start",
        # "journey_end",
        "seats",
        "invoice_number",
        "transaction_id",
        "rating",
        "payment_status",
        "payment_link",
        "amount",
    ]
    pass
