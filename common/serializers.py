from rest_framework import serializers
from . import models
# from django.db import transaction
# from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class MediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Media
        fields = [
            "file",
        ]

