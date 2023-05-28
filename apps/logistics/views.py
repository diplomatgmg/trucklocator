from rest_framework import generics

from apps.logistics.filters import CargoFilter
from apps.logistics.models import Cargo, Truck
from apps.logistics.serializers import (
    CargoListSerializer,
    CargoCreateSerializer,
    CargoRetrieveUpdateDestroySerializer,
    TruckSerializer,
)


class TruckUpdateAPIView(generics.UpdateAPIView):
    serializer_class = TruckSerializer
    queryset = Truck.objects.all()


class CargoListAPIView(generics.ListAPIView):
    serializer_class = CargoListSerializer
    filterset_class = CargoFilter

    def get_queryset(self):
        queryset = (
            Cargo.objects.all()
            .select_related("pickup_location", "delivery_location")
            .only(
                "pickup_location__latitude",
                "pickup_location__longitude",
                "pickup_location__city",
                "pickup_location__state",
                "delivery_location__city",
                "delivery_location__state",
                "weight",
            )
        )

        return queryset


class CargoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CargoRetrieveUpdateDestroySerializer

    def get_queryset(self):
        queryset = (
            Cargo.objects.all()
            .select_related("pickup_location", "delivery_location")
            .only(
                "pickup_location__latitude",
                "pickup_location__longitude",
                "pickup_location__city",
                "pickup_location__state",
                "delivery_location__city",
                "delivery_location__state",
                "weight",
                "description",
            )
        )
        return queryset


class CargoCreateAPIView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
    queryset = Cargo.objects.all()
