from django.contrib import admin

from apps.logistics.models import Location, Cargo, Truck


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "zip_code", "latitude", "longitude")
    search_fields = ("city", "state", "zip_code")


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ("id", "pickup_location", "delivery_location", "weight")
    list_select_related = ("pickup_location", "delivery_location")


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("id", "number", "location", "load_capacity")
    list_select_related = ("location",)
    search_fields = ("id", "number", "location__city", "location__state")
