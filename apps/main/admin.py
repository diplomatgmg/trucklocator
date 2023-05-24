from django.contrib import admin

from apps.main.models import Location, Cargo, Truck


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("city", "state", "zip_code", "latitude", "longitude")
    search_fields = ("city", "state", "zip_code")


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    list_display = ("number", "location", "load_capacity")
    list_select_related = ("location",)
    search_fields = ("number", "location__city", "location__state")
