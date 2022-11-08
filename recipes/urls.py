from django.urls import path

from . import views

urlpatterns = [
    path("", views.read_all_recipes, name="read-all-recipes"),
    path("ready/", views.read_ready_recipes, name="read-ready-recipes"),
    path("<int:id>/", views.read_recipe, name="read-recipe"),
    path("create/", views.create_recipe, name="create-recipe"),
    path("cook/<int:id>/", views.cook_recipe, name="cook-recipe"),
    path("update/<int:id>/", views.update_recipe, name="update-recipe"),
    path("delete/<int:id>/", views.delete_recipe, name="delete-recipe"),
]
