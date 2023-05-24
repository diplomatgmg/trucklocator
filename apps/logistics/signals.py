import csv

from django.db.models.signals import post_migrate, pre_save
from django.dispatch import receiver

from apps.logistics.models import Location, Truck


@receiver(post_migrate)
def load_locations(sender, **kwargs):
    if sender.name == "apps.logistics":
        with open("uszips.csv", "r") as file:
            reader = csv.DictReader(file)

            for row in reader:
                city = row["city"]
                state = row["state_name"]
                zip_code = row["zip"]
                latitude = row["lat"]
                longitude = row["lng"]

                Location.objects.get_or_create(
                    city=city,
                    state=state,
                    zip_code=zip_code,
                    latitude=latitude,
                    longitude=longitude,
                )

                if reader.line_num == 3000:
                    print("3000 locations successfully loaded")
                    break


@receiver(pre_save, sender=Truck)
def set_truck_random_location(sender, instance, **kwargs):
    if not instance.location:
        random_location = Location.objects.order_by("?").first()
        instance.location = random_location
