from django.contrib import admin

from apps.main.models import Location, Cargo, Truck


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    pass


@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    pass


@admin.register(Truck)
class TruckAdmin(admin.ModelAdmin):
    pass
