from django.apps import AppConfig
from django.db.models.signals import post_migrate, pre_save


class MainConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.main"

    def ready(self):
        from apps.main.signals import load_locations, set_truck_random_location
        from apps.main.models import Truck

        post_migrate.connect(load_locations)
        pre_save.connect(set_truck_random_location, sender=Truck)
        print("pre save connected")
