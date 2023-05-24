from django.core.validators import MinLengthValidator, MaxLengthValidator
from geopy.distance import geodesic
from rest_framework import serializers

from apps.logistics.models import Cargo, Location, Truck


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CargoListSerializer(serializers.ModelSerializer):
    pickup_location = serializers.StringRelatedField()
    delivery_location = serializers.StringRelatedField()
    count_nearest_trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = (
            "pickup_location",
            "delivery_location",
            "nearest_trucks",
        )

    def get_count_nearest_trucks(self, obj):
        return obj.nearest_trucks_count


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
