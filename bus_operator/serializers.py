from rest_framework import serializers
from . import models
from django.contrib.auth import password_validation
from django.db import transaction
from django.db import IntegrityError
from django.contrib.auth import get_user_model

User = get_user_model()


class BusOperatorProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source="user.full_name", read_only=False)
    email = serializers.CharField(source="user.email", read_only=False)
    phone_number = serializers.CharField(source="user.phone_number", read_only=False)
    password = serializers.CharField(write_only=True, required=False)
    approval_status = serializers.CharField(read_only=True)
    rejection_comment = serializers.CharField(read_only=True)

    class Meta:
        model = models.BusOperatorProfile
        fields = [
            "id",
            "full_name",
            "password",
            "email",
            "phone_number",
            "business_name",
            "business_logo",
            "office_address",
            "ratings",
            "approval_status",
            "rejection_comment",
        ]

    @transaction.atomic
    def create(self, validated_data):
        if "user" in validated_data:
            # Validate Mandatory Fields
            if "email" not in validated_data["user"]:
                raise serializers.ValidationError(
                    {"success": False, "errors": {"email": ["This field is required."]}}
                )
            if "full_name" not in validated_data["user"]:
                raise serializers.ValidationError(
                    {
                        "success": False,
                        "errors": {"full_name": ["This field is required."]},
                    }
                )
            if "password" not in validated_data:
                raise serializers.ValidationError(
                    {
                        "success": False,
                        "errors": {"password": ["This field is required."]},
                    }
                )

            # Create User Objects
            try:
                password = validated_data.pop("password")
                user = User.objects.create(
                    role="BUS_OPERATOR", **validated_data["user"]
                )
                user.set_password(password)
                user.save()
                del validated_data["user"]

            except IntegrityError as e:
                raise serializers.ValidationError(
                    {
                        "success": False,
                        "errors": ["user with given email id already exists"],
                    }
                )
        else:
            raise serializers.ValidationError(
                {
                    "success": False,
                    "errors": {
                        "full_name": ["This field is required."],
                        "email": ["This field is required."],
                        "phone_number": ["This field is required."],
                    },
                }
            )
        instance = models.BusOperatorProfile.objects.create(user=user, **validated_data)
        return instance

    def update(self, instance, validated_data):
        if "user" in validated_data:
            instance.user.full_name = validated_data["user"].get(
                "full_name", instance.user.full_name
            )
            instance.user.phone_number = validated_data["user"].get(
                "phone_number", instance.user.phone_number
            )
            del validated_data["user"]
        return super().update(instance, validated_data)

    def validate_pasword(self, value):
        password_validation.validate_password(value, self.instance)
        return value
