from django.contrib import admin
from . import models

# Inlines
class BusStoppageInline(admin.TabularInline):
    model = models.BusStoppage
    ordering = ["count"]


# Model Admin
@admin.register(models.BusOperatorProfile)
class BusOperatorProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "operator", "capacity")
    inlines = [
        BusStoppageInline,
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
