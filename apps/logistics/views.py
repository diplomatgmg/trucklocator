from rest_framework import generics

from apps.logistics.models import Cargo
from apps.logistics.serializers import CargoListSerializer, CargoCreateSerializer


class TruckListAPIView(generics.ListAPIView):
    pass


class CargoListAPIView(generics.ListAPIView):
    queryset = Cargo.objects.all()
    serializer_class = CargoListSerializer


class CargoCreateAPIView(generics.CreateAPIView):
    serializer_class = CargoCreateSerializer
