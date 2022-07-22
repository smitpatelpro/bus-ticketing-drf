from ast import operator
from asyncore import read
from importlib.metadata import requires
from typing_extensions import Required
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


class BusStoppageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusStoppage
        fields = [
            "id",
            "bus",
            "count",
            "name",
            "arrival_time",
            "departure_time",
            "distance_from_last_stop",
            "journey_type",
        ]

class BusJourneySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.BusJourney
        fields = [
            "id",
            "bus",
            "sequence",
            "from_place",
            "to_place",
            "start_time",
            "end_time",
            "distance",
            "journey_type",
        ]


class BusSerializer(serializers.ModelSerializer):
    photos = MediaSerializer(many=True, read_only=True)
    amenities = BusAmenitySerializer(many=True, read_only=True)
    operator = serializers.CharField(required=False)
    journey = BusJourneySerializer(source="busjourney_bus", many=True, read_only=True)

    class Meta:
        model = models.Bus
        fields = [
            "id",
            "name",
            "operator",
            "type",
            "capacity",
            "per_km_fare",
            "photos",
            "amenities",
            "journey",
        ]

    def create(self, validated_data):
        profile = self.context.get("profile")
        instance = models.Bus.objects.create(operator=profile, **validated_data)
        return instance


class TicketSerializer(serializers.ModelSerializer):
    payment_status = serializers.CharField(read_only=True)
    payment_link = serializers.CharField(read_only=True)
    rating = serializers.CharField(read_only=True)
    amount = serializers.CharField(read_only=True)
    transaction_id = serializers.CharField(read_only=True)
    invoice_number = serializers.CharField(read_only=True)
    class Meta:
        model = models.Ticket

        fields = [
            "id",
            "number",
            "customer",
            "bus",
            "journey_date",
            "journey_start",
            "journey_end",
            "seats",
            "invoice_number",
            "transaction_id",
            "rating",
            "payment_status",
            "payment_link",
            "amount",
        ]
    
    def validate(self, data):
        """
        Check that the journey_start and journey_end are valid bus journey stops
        """
        bus = data["bus"]
        data["journey_start"] = data["journey_start"].capitalize()
        data["journey_end"] = data["journey_end"].capitalize()
        distance = bus.get_distance(data["journey_start"], data["journey_end"])
        if not distance:
            raise serializers.ValidationError("journey_start and journey_end are not part of bus journey. please correct them.")
        data["distance"] = distance
        # print("dist:", distance)
        # if data['start_date'] > data['end_date']:
        #     raise serializers.ValidationError({"end_date": "finish must occur after start"})
        return data
    
    def create(self, validated_data):
        bus = validated_data.get("bus")
        distance = validated_data.pop("distance")
        # calculate amount
        amount = bus.calculate_amount(distance)
        validated_data["amount"] = amount

        instance = models.Ticket.objects.create(**validated_data)
        return instance

