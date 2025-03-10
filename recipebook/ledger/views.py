from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Recipe


def recipe_list(request):
    recipes = Recipe.objects.all()

    return render(request, "ledger/recipe_list.html", {"recipes":recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    return render(request, "ledger/recipe_detail.html", {"recipe": recipe})