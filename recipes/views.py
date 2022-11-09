from django.shortcuts import render
from django.http import JsonResponse
from recipes.models import Recipe, RequiredIngredient, Step
from ingredients.models import Ingredient
from django.views.decorators.csrf import csrf_exempt
import json


def check_fridge(required):
    for req in required:
        if len(Ingredient.objects.filter(ingredient_name=req.ingredient_name)) == 0:
            return False
        # TODO Quantities
    return True


def read_all_recipes(request):
    all_recipes = Recipe.objects.all()
    res = []
    for recipe in all_recipes:
        res.append(
            {
                "id": recipe.id,
                "recipeName": recipe.recipe_name,
                "ready": check_fridge(recipe.ingredients.all()),
            }
        )
    return JsonResponse({"recipes": res})


def read_ready_recipes(request):
    all_recipes = Recipe.objects.all()
    res = []

    for recipe in all_recipes:
        if check_fridge(recipe.ingredients.all()):
            res.append({"id": recipe.id, "recipeName": recipe.recipe_name})
    return JsonResponse({"recipes": res})


def read_recipe(request, id):
    recipe = Recipe.objects.get(id=id)
    print(len(Recipe.objects.filter(id=12319)))
    ingredients = recipe.ingredients.all()
    ingredients_list = []
    for ingredient in ingredients:
        vals = {}
        vals["ingredientName"] = ingredient.ingredient_name
        vals["unit"] = ingredient.unit
        vals["quantity"] = ingredient.quantity
        ingredients_list.append(vals)

    steps = recipe.step_set.all().order_by("step_number")
    steps_list = []
    for step in steps:
        steps_list.append(step.step)

    return JsonResponse(
        {
            "id": id,
            "recipe": recipe.recipe_name,
            "ingredients": ingredients_list,
            "steps": steps_list,
            "ready": check_fridge(recipe.ingredients.all()),
        }
    )


@csrf_exempt
def create_recipe(request):
    if request.method == "POST":
        data = json.loads(request.body)
        new_recipe = Recipe(recipe_name=data["recipeName"])
        new_recipe.save()

        for ingredient in data["ingredients"]:
            new_ingredient = RequiredIngredient(
                ingredient_name=ingredient["ingredientName"],
                unit=ingredient["unit"],
                quantity=ingredient["quantity"],
                recipe=new_recipe,
            )
            new_ingredient.save()

        for step in data["steps"]:
            new_step = Step(
                step_number=step["stepNumber"], step=step["step"], recipe=new_recipe
            )
            new_step.save()

        return JsonResponse({"res": "Successfully saved"})
    return JsonResponse({"error": "Not a POST"})


@csrf_exempt
def update_recipe(request, id):
    if request.method == "PUT":
        recipe = Recipe.objects.get(id=id)
        data = json.loads(request.body)

        if "recipeName" in data:
            recipe.recipe_name = data["recipeName"]
            recipe.save()

        if "ingredients" in data:
            RequiredIngredient.objects.filter(recipe=recipe).delete()
            for ingredient in data["ingredients"]:
                new_ingredient = RequiredIngredient(
                    ingredient_name=ingredient["ingredientName"],
                    unit=ingredient["unit"],
                    quantity=ingredient["quantity"],
                    recipe=recipe,
                )
                new_ingredient.save()

        if "steps" in data:
            Step.objects.filter(recipe=recipe).delete()
            for step in data["steps"]:
                new_step = Step(
                    step_number=step["stepNumber"], step=step["step"], recipe=recipe
                )
                new_step.save()

    return JsonResponse({"error": "Not a PUT"})


@csrf_exempt
def cook_recipe(request, id):
    if request.method == "PUT":
        recipe = Recipe.objects.get(id=id)
        ingredients = recipe.ingredients.all()
        for ingredient in ingredients:
            fridge_ingredient = Ingredient.objects.get(
                ingredient_name=ingredient.ingredient_name
            )
            # TODO Unit matching
            fridge_ingredient.quantity -= ingredient.quantity
            if fridge_ingredient.quantity <= 0:
                fridge_ingredient.delete()
            else:
                fridge_ingredient.save()
        return JsonResponse({"res": "Success"})
    return JsonResponse({"error": "Not a PUT"})


@csrf_exempt
def delete_recipe(request, id):
    if request.method == "DELETE":
        Recipe.objects.filter(id=id).delete()
        return JsonResponse({"res": "Successful deletion"})
    return JsonResponse({"error": "Not a DELETE"})
