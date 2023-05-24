from django.urls import path

from apps.main.views import TruckAPIListView

app_name = "trucks"

urlpatterns = [
    path("", TruckAPIListView.as_view(), name="truck-list"),
]
