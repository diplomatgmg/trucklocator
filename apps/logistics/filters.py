import django_filters
from django.utils.translation import gettext_lazy as _

from apps.logistics.models import Cargo


class CargoFilter(django_filters.FilterSet):
    weight = django_filters.RangeFilter()
    min_distance_to_trucks = django_filters.NumberFilter(
        label=_("Минимальная дистанция до машины"),
        method="filter_min_distance_to_trucks",

    )
    max_distance_to_trucks = django_filters.NumberFilter(
        label=_("Максимальная дистанция до машины"),
        method="filter_max_distance_to_trucks",

    )

    class Meta:
        model = Cargo
        fields = ("weight", "min_distance_to_trucks", "max_distance_to_trucks")

    def filter_min_distance_to_trucks(self, queryset, name, value):
        return queryset

    def filter_max_distance_to_trucks(self, queryset, name, value):
        return queryset
