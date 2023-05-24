from django.urls import path

from apps.logistics.views import TruckListAPIView, CargoListAPIView, CargoCreateAPIView

app_name = "logistics"

urlpatterns = [
    path("truck/", TruckListAPIView.as_view(), name="truck-list"),
    path("cargo/", CargoListAPIView.as_view(), name="cargo-list"),
    path("cargo/create/", CargoCreateAPIView.as_view(), name="cargo-create"),
]
