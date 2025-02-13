from django.shortcuts import render

# Context data for recipes
RECIPES = [
    {
        "name": "Recipe 1",
        "ingredients": [
            {"name": "tomato", "quantity": "3pcs"},
            {"name": "onion", "quantity": "1pc"},
            {"name": "pork", "quantity": "1kg"},
            {"name": "water", "quantity": "1L"},
            {"name": "sinigang mix", "quantity": "1 packet"},
        ],
        "link": "/recipe/1"
    },
    {
        "name": "Recipe 2",
        "ingredients": [
            {"name": "garlic", "quantity": "1 head"},
            {"name": "onion", "quantity": "1pc"},
            {"name": "vinegar", "quantity": "1/2cup"},
            {"name": "water", "quantity": "1 cup"},
            {"name": "salt", "quantity": "1 tablespoon"},
            {"name": "whole black peppers", "quantity": "1 tablespoon"},
            {"name": "pork", "quantity": "1 kilo"},
        ],
        "link": "/recipe/2"
    }
]

# View for listing recipes
def recipe_list(request):
    return render(request, "recipe_list.html", {"recipes": RECIPES})

# View for individual recipe details
def recipe_detail(request, recipe_id):
    recipe = next((r for r in RECIPES if r["link"] == f"/recipe/{recipe_id}"), None)
    return render(request, "recipe_detail.html", {"recipe": recipe})
