from django.contrib import admin
from .models import User, Media

# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Media)
class MediaAdmin(admin.ModelAdmin):
    pass
