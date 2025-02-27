from django.urls import path
from .views import recipe_list, recipe_detail

app_name = "ledger"

urlpatterns = [
    path("recipes/list/", recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', recipe_detail, name='recipe_detail'),
]
