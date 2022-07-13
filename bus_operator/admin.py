from django.contrib import admin
from .models import BusOperatorProfile


@admin.register(BusOperatorProfile)
class BusOperatorProfileAdmin(admin.ModelAdmin):
    pass
