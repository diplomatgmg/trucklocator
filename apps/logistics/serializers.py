from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from geopy.distance import geodesic
from rest_framework import serializers

from apps.logistics.models import Cargo, Truck
from apps.logistics.services import get_location_by_zip


class TruckSerializer(serializers.ModelSerializer):
    location_zip = serializers.CharField(
        validators=(MinLengthValidator(5), MaxLengthValidator(5)),
        label=_("Почтовый индекс"),
        source='location'
    )

    class Meta:
        model = Truck
        fields = ("location_zip",)

    def update(self, instance, validated_data):
        location = get_location_by_zip(validated_data['location'])
        instance.location = location
        instance.save()
        return instance


class BaseCargoSerializer(serializers.ModelSerializer):
    _trucks = None

    def __init__(self, *args, **kwargs):
        self._trucks = (
            Truck.objects.all()
            .select_related("location")
            .only(
                "number",
                "location__latitude",
                "location__longitude",
            )
        )
        super().__init__(*args, **kwargs)

    def get_pickup_location(self, obj):
        return f"{obj.pickup_location.city} / {obj.pickup_location.state}"

    def get_delivery_location(self, obj):
        return f"{obj.delivery_location.city} / {obj.delivery_location.state}"

    def get_nearby_trucks(self, obj):
        cargo_coordinates = (
            obj.pickup_location.latitude,
            obj.pickup_location.longitude,
        )

        nearest_trucks = []

        for truck in self._trucks:
            truck_coordinates = (truck.location.latitude, truck.location.longitude)
            distance = geodesic(cargo_coordinates, truck_coordinates).miles

            if distance <= 450:
                nearest_trucks.append([truck, distance])

        return nearest_trucks


class CargoListSerializer(BaseCargoSerializer):
    number_nearby_trucks = serializers.SerializerMethodField()
    pickup_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = (
            "pickup_location",
            "delivery_location",
            "number_nearby_trucks",
        )

    def get_number_nearby_trucks(self, obj):
        return len(self.get_nearby_trucks(obj))


class CargoRetrieveUpdateDestroySerializer(BaseCargoSerializer):
    pickup_location = serializers.SerializerMethodField()
    delivery_location = serializers.SerializerMethodField()
    trucks = serializers.SerializerMethodField()

    class Meta:
        model = Cargo
        fields = (
            "pickup_location",
            "delivery_location",
            "weight",
            "description",
            "trucks",
        )

    def get_trucks(self, obj):
        trucks = self.get_nearby_trucks(obj)

        return [
            {"number": truck.number, "distance": round(distance, 2)}
            for truck, distance in trucks
        ]


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
        pickup_location_zip = get_location_by_zip(validated_data["pickup_location_zip"])
        delivery_location_zip = get_location_by_zip(
            validated_data["delivery_location_zip"]
        )

        cargo = Cargo(
            pickup_location=pickup_location_zip,
            delivery_location=delivery_location_zip,
            weight=validated_data["weight"],
            description=validated_data["description"],
        )
        cargo.save()
        return cargo
