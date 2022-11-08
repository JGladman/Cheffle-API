from django.db import models


class Recipe(models.Model):
    recipe_name = models.CharField(max_length=64)


class RequiredIngredient(models.Model):
    ingredient_name = models.CharField(max_length=64)
    unit = models.CharField(max_length=6)
    quantity = models.FloatField()
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name="ingredients"
    )


class Step(models.Model):
    step_number = models.IntegerField()
    step = models.TextField()
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
