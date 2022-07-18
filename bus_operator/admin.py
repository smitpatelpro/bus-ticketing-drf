from django.contrib import admin
from . import models


@admin.register(models.BusOperatorProfile)
class BusOperatorProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bus)
class BusAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusAmenity)
class BusAmenityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusStoppage)
class BusStoppageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BusUnavailability)
class BusUnavailabilityAdmin(admin.ModelAdmin):
    pass
