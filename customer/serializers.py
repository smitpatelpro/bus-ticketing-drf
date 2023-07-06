from rest_framework import serializers
from . import models
from django.contrib.auth import password_validation
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth import get_user_model
from common.serializers import MediaSerializer
from common.models import Media

User = get_user_model()


class CustomerProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(
        source="user.full_name", read_only=False, required=True
    )
    email = serializers.CharField(source="user.email", read_only=False, required=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=False)
    password = serializers.CharField(write_only=True, required=True)
    id_proof = MediaSerializer(read_only=True)
    address_proof = MediaSerializer(read_only=True)
    other_kyc_document = MediaSerializer(read_only=True)

    class Meta:
        model = models.CustomerProfile
        fields = [
            "id",
            "full_name",
            "password",
            "email",
            "phone_number",
            "gender",
            "address",
            "id_proof",
            "address_proof",
            "other_kyc_document",
        ]

    # Check for weak passwords
    def validate_password(self, value):
        password_validation.validate_password(value, self.instance)
        return value

    def validate_email(self, value):
        request = self.context.get("request", None)
        if request and getattr(request, "method", None) == "POST":
            users = User.objects.filter(email=value)
            if users.exists():
                raise serializers.ValidationError(
                    {
                        "success": False,
                        "errors": ["user with given email id already exists"],
                    }
                )
        return value

    @transaction.atomic
    def create(self, validated_data):
        # Create User Objects
        password = validated_data.pop("password")
        user = User.objects.create(role="BUS_OPERATOR", **validated_data["user"])
        user.set_password(password)
        user.save()
        del validated_data["user"]

        instance = models.CustomerProfile.objects.create(user=user, **validated_data)
        return instance

    def update(self, instance, validated_data):
        if "user" in validated_data:
            instance.user.full_name = validated_data["user"].get(
                "full_name", instance.user.full_name
            )
            instance.user.phone_number = validated_data["user"].get(
                "phone_number", instance.user.phone_number
            )
            # Email is only allowed to set in POST request, So, we are not updating it here.
            del validated_data["user"]  # Drop related user data for normal updation.
        return super().update(instance, validated_data)


class CustomerProfileMediaSerializer(serializers.ModelSerializer):
    id_proof = MediaSerializer()
    address_proof = MediaSerializer()
    other_kyc_document = MediaSerializer()

    class Meta:
        model = models.CustomerProfile
        fields = [
            "id_proof",
            "address_proof",
            "other_kyc_document",
        ]

    def update(self, instance, validated_data):
        # if media objects present, then delete existing and create new one
        if "id_proof" in validated_data:
            if instance.id_proof:
                instance.id_proof.delete()
            media = Media.objects.create(file=validated_data["id_proof"]["file"])
            instance.id_proof = media

        if "address_proof" in validated_data:
            if instance.address_proof:
                instance.address_proof.delete()
            media = Media.objects.create(file=validated_data["address_proof"]["file"])
            instance.address_proof = media

        if "other_kyc_document" in validated_data:
            if instance.other_kyc_document:
                instance.other_kyc_document.delete()
            media = Media.objects.create(
                file=validated_data["other_kyc_document"]["file"]
            )
            instance.other_kyc_document = media

        instance.save(update_fields=["id_proof", "address_proof", "other_kyc_document"])
        return instance
