from django.contrib import admin
from . import models


@admin.register(models.BusOperatorProfile)
class BusOperatorProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Bus)
class BusOperatorProfileAdmin(admin.ModelAdmin):
    pass
