from rest_framework import serializers
from . import models

from django.contrib.auth import get_user_model

User = get_user_model()


class MediaSerializer(serializers.ModelSerializer):
    file = serializers.FileField(required=True)

    class Meta:
        model = models.Media
        fields = [
            "id",
            "file",
            "created_at",
            "updated_at",
        ]
