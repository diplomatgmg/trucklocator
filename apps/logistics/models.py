import random
import string

from django.core.validators import (
    MinValueValidator,
    MaxValueValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class Location(models.Model):
    latitude = models.FloatField(_("Географическая широта"))
    longitude = models.FloatField(_("Географическая долгота"))
    city = models.CharField(_("Город"), max_length=100)
    state = models.CharField(_("Штат"), max_length=100)
    zip_code = models.CharField(
        _("Почтовый индекс"),
        unique=True,
        validators=(MinLengthValidator(5), MaxLengthValidator(5)),
    )

    def __str__(self):
        return f"Location #{self.id}"

    class Meta:
        verbose_name = _("Локация")
        verbose_name_plural = _("Локации")


class Cargo(models.Model):
    pickup_location = models.ForeignKey(
        Location,
        models.SET_NULL,
        verbose_name=_("Локация отгрузки"),
        null=True,
        blank=True,
        related_name="pickup_cargo_set",
        db_index=True,
    )
    delivery_location = models.ForeignKey(
        Location,
        models.SET_NULL,
        verbose_name=_("Локация доставки"),
        null=True,
        blank=True,
        related_name="delivery_cargo_set",
        db_index=True,
    )
    weight = models.PositiveIntegerField(
        _("Вес"), default=1, validators=(MinValueValidator(1), MaxValueValidator(1000))
    )
    description = models.TextField(_("Описание"), blank=True)

    def __str__(self):
        return f"Cargo #{self.pk}"

    class Meta:
        verbose_name = _("Груз")
        verbose_name_plural = _("Грузы")


def generate_truck_number():
    unique_number = str(random.randint(1000, 9999)) + random.choice(
        string.ascii_uppercase
    )
    return unique_number


class Truck(models.Model):
    location = models.ForeignKey(
        Location,
        models.SET_NULL,
        null=True,
        blank=True,
        db_index=True,
    )
    load_capacity = models.PositiveIntegerField(
        default=1, validators=(MinValueValidator(1), MaxValueValidator(1000))
    )

    number = models.CharField(max_length=5, unique=True, default=generate_truck_number)

    def __str__(self):
        return f"Truck #{self.id}"

    class Meta:
        verbose_name = _("Грузовик")
        verbose_name_plural = _("Грузовики")
