from django.urls import path
from .views import recipe_list, recipe_detail, AddRecipeView, AddImageView


app_name = "ledger"

urlpatterns = [
    path("recipes/list/", recipe_list, name="recipe_list"),
    path("recipe/<int:recipe_id>/", recipe_detail, name="recipe_detail"),
    path("recipe/add/", AddRecipeView.as_view(), name="add_recipe"),
    path("recipe/<int:recipe_id>/add_image/", AddImageView.as_view(), name="add_image"),
]
