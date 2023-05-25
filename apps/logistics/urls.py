from django.urls import path

from apps.logistics.views import (
    TruckUpdateAPIView,
    CargoListAPIView,
    CargoCreateAPIView,
    CargoRetrieveUpdateDestroyAPIView,
)

app_name = "logistics"

urlpatterns = [
    path("truck/<int:pk>", TruckUpdateAPIView.as_view(), name="truck-update"),
    path("cargo/", CargoListAPIView.as_view(), name="cargo-list"),
    path(
        "cargo/<int:pk>",
        CargoRetrieveUpdateDestroyAPIView.as_view(),
        name="cargo-detail",
    ),
    path("cargo/create/", CargoCreateAPIView.as_view(), name="cargo-create"),
]
