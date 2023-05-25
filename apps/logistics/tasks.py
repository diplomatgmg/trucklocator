from celery import shared_task

from apps.logistics.models import Truck, Location


@shared_task
def update_truck_locations():
    trucks = Truck.objects.all()

    for truck in trucks:
        random_location = Location.objects.order_by("?").first()
        truck.location = random_location
        truck.save()
