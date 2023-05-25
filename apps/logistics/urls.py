from django.urls import path

from apps.logistics.views import (
    TruckListAPIView,
    CargoListAPIView,
    CargoCreateAPIView,
    CargoRetrieveUpdateDestroyAPIView,
)

app_name = "logistics"

urlpatterns = [
    path("truck/", TruckListAPIView.as_view(), name="truck-list"),
    path("cargo/", CargoListAPIView.as_view(), name="cargo-list"),
    path("cargo/<int:pk>", CargoRetrieveUpdateDestroyAPIView.as_view(), name="cargo-detail"),
    path("cargo/create/", CargoCreateAPIView.as_view(), name="cargo-create"),
]
