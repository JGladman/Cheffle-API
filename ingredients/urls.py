from django.urls import path

from . import views

urlpatterns = [
    path("", views.read_all_ingredients, name="view-all-ingredients"),
    path("create/", views.create_ingredients, name="create-ingredient"),
    path("update/", views.update_ingredients, name="update-ingredients"),
    path("delete/", views.delete_ingredients, name="delete-ingredient"),
]
