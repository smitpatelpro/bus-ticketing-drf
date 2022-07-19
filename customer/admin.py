from django.contrib import admin
from . import models


@admin.register(models.CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    pass
