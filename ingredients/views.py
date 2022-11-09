from django.shortcuts import render
from django.http import JsonResponse
from ingredients.models import Ingredient
from django.views.decorators.csrf import csrf_exempt
import json


def read_all_ingredients(request):
    all_ingredients = Ingredient.objects.all()
    res = []
    for ingredient in all_ingredients:
        obj = {}
        obj["id"] = ingredient.id
        obj["ingredientName"] = ingredient.ingredient_name
        obj["unit"] = ingredient.unit
        obj["quantity"] = ingredient.quantity
        res.append(obj)
    unit = "imperial"
    if all_ingredients[0].unit in ["mg", "g", "kg", "ml", "l"]:
        unit = "metric"
    return JsonResponse({"ingredients": res, "unit": unit})


@csrf_exempt
def create_ingredients(request):
    if request.method == "POST":
        data = json.loads(request.body)
        for new in data["new"]:
            Ingredient(
                ingredient_name=new["ingredientName"],
                unit=new["unit"],
                quantity=new["quantity"],
            ).save()
        return JsonResponse({"res": "Success"})
    return JsonResponse({"Error": "Not a POST"})


@csrf_exempt
def update_ingredients(request):
    if request.method == "PUT":
        data = json.loads(request.body)
        for change in data["changes"]:
            ingredient = Ingredient.objects.get(id=change["id"])
            if "ingredientName" in change:
                ingredient.ingredient_name = change["ingredientName"]
            if "unit" in change:
                ingredient.unit = change["unit"]
            if "quantity" in change:
                ingredient.quantity = change["quantity"]
            ingredient.save()
        return JsonResponse({"res": "Success"})
    return JsonResponse({"Error": "Not a PUT"})


@csrf_exempt
def delete_ingredients(request):
    if request.method == "DELETE":
        data = json.loads(request.body)
        for id in data["ids"]:
            Ingredient.objects.filter(id=id).delete()
        return JsonResponse({"res": "Success"})
    return JsonResponse({"Error": "Not a DELETE"})
