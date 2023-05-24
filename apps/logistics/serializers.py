from django.core.validators import MinLengthValidator, MaxLengthValidator
from rest_framework import serializers

from apps.logistics.models import Cargo, Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CargoListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cargo
        fields = "__all__"


class CargoCreateSerializer(serializers.ModelSerializer):
    pickup_location_zip = serializers.CharField(
        validators=(MinLengthValidator(5), MaxLengthValidator(5))
    )
    delivery_location_zip = serializers.CharField(
        validators=(MinLengthValidator(5), MaxLengthValidator(5))
    )

    class Meta:
        model = Cargo
        fields = (
            "pickup_location_zip",
            "delivery_location_zip",
            "weight",
            "description",
        )

    def save(self, **kwargs):
        pickup_location_zip = Location.objects.get(
            zip_code=self.validated_data["pickup_location_zip"]
        )
        delivery_location_zip = Location.objects.get(
            zip_code=self.validated_data["delivery_location_zip"]
        )
        weight = self.validated_data["weight"]
        description = self.validated_data["description"]
        Cargo.objects.create(
            pickup_location=pickup_location_zip,
            delivery_location=delivery_location_zip,
            weight=weight,
            description=description,
        )
