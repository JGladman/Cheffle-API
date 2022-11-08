from django.contrib import admin

from .models import Recipe, RequiredIngredient, Step

admin.site.register(Recipe)
admin.site.register(RequiredIngredient)
admin.site.register(Step)
