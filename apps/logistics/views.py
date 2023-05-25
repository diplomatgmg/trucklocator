from rest_framework import generics

from apps.logistics.models import Cargo
from apps.logistics.serializers import (
    CargoListSerializer,
    CargoCreateSerializer,
    CargoRetrieveSerializer,
)


class TruckListAPIView(generics.ListAPIView):
    pass


class CargoListAPIView(generics.ListAPIView):
    serializer_class = CargoListSerializer

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
            )
        )

        return queryset


class CargoRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = CargoRetrieveSerializer

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
