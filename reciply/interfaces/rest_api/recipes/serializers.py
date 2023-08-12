# Standard library imports
import typing

# Third party imports
from rest_framework import serializers
from rest_framework.utils import serializer_helpers

# Local application imports
from data.recipes import models as recipe_models
from domain.recipes import queries


class _RecipeBase(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=128)
    description = serializers.CharField(required=False)


class RecipeList(_RecipeBase):
    hero_image_source = serializers.SerializerMethodField(read_only=True)

    def get_hero_image_source(self, recipe: recipe_models.Recipe) -> str | None:
        if image := queries.get_hero_image(recipe):
            source = queries.get_image_source(recipe_image=image)
            print("SOURCE: ", source)
            return source
        return None


class _RecipeImage(serializers.Serializer):
    id = serializers.IntegerField()
    image_source = serializers.SerializerMethodField()
    is_hero = serializers.BooleanField()

    def get_image_source(self, recipe_image: recipe_models.RecipeImage) -> str:
        return queries.get_image_source(recipe_image=recipe_image)


class RecipeDetail(RecipeList):
    images = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

    def get_images(
        self, recipe: recipe_models.Recipe
    ) -> list[serializer_helpers.ReturnDict]:
        images = recipe.images.order_by("-is_hero")  # Put the hero image first
        return typing.cast(
            list[serializer_helpers.ReturnDict],
            _RecipeImage(instance=images, many=True).data,
        )


class RecipeCreate(_RecipeBase):
    hero_image = serializers.ImageField(required=False)
