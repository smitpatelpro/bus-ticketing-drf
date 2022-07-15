from ast import operator
from asyncore import read
from rest_framework import serializers
from . import models
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from common.serializers import MediaSerializer
from common.models import Media

User = get_user_model()


class BusOperatorOverviewSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=False)
    email = serializers.CharField(source="user.email", read_only=False)
    phone_number = serializers.CharField(source="user.phone_number", read_only=False)
    business_logo = serializers.SerializerMethodField()

    class Meta:
        model = models.BusOperatorProfile
        fields = [
            "id",
            "full_name",
            "email",
            "phone_number",
            "business_name",
            "business_logo",
            "office_address",
            "ratings",
        ]

    def get_business_logo(self, obj):
        return (
            obj.business_logo.file.url
            if obj.business_logo and obj.business_logo.file
            else ""
        )


class BusAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusAmenity
        fields = [
            "id",
            "name",
            "description",
        ]


class BusSerializer(serializers.ModelSerializer):
    photos = MediaSerializer(many=True, read_only=True)
    amenities = BusAmenitySerializer(many=True, read_only=True)

    class Meta:
        model = models.Bus
        fields = [
            "id",
            "name",
            "type",
            "capacity",
            "per_km_fare",
            "photos",
            "amenities",
        ]

    def create(self, validated_data):
        profile = self.context.get("profile")
        instance = models.Bus.objects.create(operator=profile, **validated_data)
        return instance
