from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.logistics.models import Location


def get_location_by_zip(zip_code):
    try:
        location = Location.objects.get(zip_code=zip_code)
        return location
    except Location.DoesNotExist:
        raise serializers.ValidationError(_("Введён неверный почтовый индекс"))
