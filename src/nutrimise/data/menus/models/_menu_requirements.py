from django.db import models as django_models

from nutrimise.data import constants

from . import _menu


class MenuRequirements(django_models.Model):
    """
    The requirements to meet when optimising a menu.
    """

    menu = django_models.OneToOneField(
        _menu.Menu, on_delete=django_models.CASCADE, related_name="requirements"
    )

    maximum_occurrences_per_recipe = django_models.SmallIntegerField()

    dietary_requirements = django_models.ManyToManyField(
        "ingredients.DietaryRequirement", related_name="+", blank=True
    )

    def __str__(self) -> str:
        return f"Requirements for '{self.menu.name}'"


class NutrientRequirement(django_models.Model):
    """
    The nutrient requirements to meet when optimising a menu.
    """

    id = django_models.AutoField(primary_key=True)

    menu_requirements = django_models.ForeignKey(
        MenuRequirements,
        on_delete=django_models.CASCADE,
        related_name="nutrient_requirements",
    )

    nutrient = django_models.ForeignKey(
        "ingredients.Nutrient", on_delete=django_models.PROTECT, related_name="+"
    )

    minimum_quantity = django_models.FloatField(null=True, blank=True)

    maximum_quantity = django_models.FloatField(null=True, blank=True)

    target_quantity = django_models.FloatField(null=True, blank=True)

    units = django_models.TextField(choices=constants.NutrientUnit.choices)

    enforcement_interval = django_models.TextField(
        choices=constants.NutrientRequirementEnforcementInterval.choices
    )