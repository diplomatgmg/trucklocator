import csv

from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.main.models import Location


@receiver(post_migrate)
def load_locations(sender, **kwargs):
    if sender.name == "apps.main":
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
