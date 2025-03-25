from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from .models import Recipe, RecipeIngredient, Ingredient, RecipeImage
from .forms import RecipeForm, RecipeIngredientForm, RecipeImageForm, inlineformset_factory

def recipe_list(request):
    recipes = Recipe.objects.all()
    return render(request, "ledger/recipe_list.html", {"recipes": recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    return render(request, "ledger/recipe_detail.html", {"recipe": recipe})

class AddRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "ledger/add_recipe.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context["entered_recipe_name"] = self.request.session.get("entered_recipe_name", "")
        context["entered_ingredients"] = self.request.session.get("entered_ingredients", [])
        
        return context

    def post(self, request, *args, **kwargs):
        """Handles both adding ingredients and final saving of the recipe"""
        form = self.get_form()

        if "add_ingredient" in request.POST:
            recipe_name = request.POST.get("name")
            ingredient_name = request.POST.get("new_ingredient")
            quantity = request.POST.get("quantity")

            if recipe_name:
                request.session["entered_recipe_name"] = recipe_name
            
            if ingredient_name and quantity:
                # Store ingredients temporarily in session
                entered_ingredients = request.session.get("entered_ingredients", [])
                entered_ingredients.append(f"{ingredient_name} - {quantity}")
                request.session["entered_ingredients"] = entered_ingredients
                request.session.modified = True  # Mark session as changed
                
            return redirect("ledger:add_recipe")  # Stay on the same page
        
        elif form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user  
            recipe.save()

            # Add last entered ingredient before saving
            ingredient_name = request.POST.get("new_ingredient")
            quantity = request.POST.get("quantity")
            if ingredient_name and quantity:
                entered_ingredients = request.session.get("entered_ingredients", [])
                entered_ingredients.append(f"{ingredient_name} - {quantity}")
                request.session["entered_ingredients"] = entered_ingredients

            # Save entered ingredients to the database
            for entry in entered_ingredients:
                ingredient_name, quantity = entry.split(" - ")
                ingredient, _ = Ingredient.objects.get_or_create(name=ingredient_name)
                RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, quantity=quantity)

            # Clear session data
            request.session["entered_ingredients"] = []
            request.session["entered_recipe_name"] = ""

            return redirect("ledger:recipe_list")

        return self.form_invalid(form)


class AddImageView(CreateView):
    model = RecipeImage
    form_class = RecipeImageForm
    template_name = "ledger/add_image.html"

    def form_valid(self, form):
        form.instance.recipe = get_object_or_404(Recipe, id=self.kwargs["recipe_id"])
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["recipe"] = get_object_or_404(Recipe, id=self.kwargs["recipe_id"])  # ✅ Pass recipe to the template
        return context

    def get_success_url(self):
        return reverse_lazy("ledger:recipe_detail", kwargs={"recipe_id": self.kwargs["recipe_id"]})