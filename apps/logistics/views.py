from rest_framework import generics

from apps.logistics.models import Cargo
from apps.logistics.serializers import CargoListSerializer, CargoCreateSerializer


class TruckListAPIView(generics.ListAPIView):
    pass


class CargoListAPIView(generics.ListAPIView):
    serializer_class = CargoListSerializer

    def get_queryset(self):
        queryset = Cargo.objects.all().select_related(
            "pickup_location", "delivery_location"
        )
        return queryset


class CargoCreateAPIView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
