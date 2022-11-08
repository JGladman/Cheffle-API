from django.urls import path

from . import views

urlpatterns = [
    path("", views.view_all_ingredients, name="view-all-ingredients"),
]
