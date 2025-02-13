from django.urls import path
from . import views

app_name = "ledger"

urlpatterns = [
    path('', views.recipe_list, name='recipe_list'),  # This makes / point to recipes list
    path('recipes/list/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:recipe_id>/', views.recipe_detail, name='recipe_detail'),
]
