from django.shortcuts import render
from django.http import JsonResponse
from ingredients.models import Ingredient


def view_all_ingredients(request):
    all_ingredients = Ingredient.objects.all()
    res = []
    for ingredient in all_ingredients:
        obj = {}
        obj["ingredient_name"] = ingredient.ingredient_name
        obj["unit"] = ingredient.unit
        obj["quantity"] = ingredient.quantity
        res.append(obj)
    return JsonResponse({"Ingredients": res})
