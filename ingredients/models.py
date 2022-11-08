from django.db import models

# Create your models here.
class Ingredient(models.Model):
    ingredient_name = models.CharField(max_length=64)
    unit = models.CharField(max_length=6)
    quantity = models.FloatField()
