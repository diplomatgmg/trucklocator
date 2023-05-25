from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from geopy.distance import geodesic
from rest_framework import serializers

from apps.logistics.models import Cargo, Location, Truck


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class CargoListSerializer(serializers.ModelSerializer):
    count_nearest_trucks = serializers.SerializerMethodField()
    trucks = None

    def __init__(self, *args, **kwargs):
        self.trucks = (
            Truck.objects.select_related("location")
            .filter(location__isnull=False)
            .only("location__latitude", "location__longitude")
        )
        super().__init__(*args, **kwargs)

    class Meta:
        model = Cargo
        fields = ["pickup_location", "delivery_location", "count_nearest_trucks"]

    def get_count_nearest_trucks(self, cargo):
        cargo_coordinates = (
            cargo.pickup_location.latitude,
            cargo.pickup_location.longitude,
        )
        count_nearest_trucks = 0

        for truck in self.trucks:
            truck_coordinates = (truck.location.latitude, truck.location.longitude)
            distance = geodesic(cargo_coordinates, truck_coordinates).miles

            if distance <= 450:
                count_nearest_trucks += 1

        return count_nearest_trucks


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

    def create(self, validated_data):
        try:
            pickup_location_zip = Location.objects.get(
                zip_code=validated_data["pickup_location_zip"]
            )
            delivery_location_zip = Location.objects.get(
                zip_code=validated_data["delivery_location_zip"]
            )

        except ObjectDoesNotExist:
            raise serializers.ValidationError(_("Введён неверный почтовый индекс"))

        cargo = Cargo(
            pickup_location=pickup_location_zip,
            delivery_location=delivery_location_zip,
            weight=validated_data["weight"],
            description=validated_data["description"],
        )
        cargo.save()
        return cargo
