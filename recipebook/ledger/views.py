from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Recipe, RecipeIngredient, Ingredient, RecipeImage
from .forms import RecipeForm, RecipeIngredientFormSet, RecipeImageForm

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
        if self.request.POST:
            context["ingredient_formset"] = RecipeIngredientFormSet(self.request.POST)
        else:
            context["ingredient_formset"] = RecipeIngredientFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        ingredient_formset = context["ingredient_formset"]
        form.instance.author = self.request.user  # ✅ Assign logged-in user as the author

        if form.is_valid() and ingredient_formset.is_valid():
            self.object = form.save()
            ingredient_formset.instance = self.object
            
            for ingredient_form in ingredient_formset:
                if ingredient_form.cleaned_data.get("new_ingredient"):
                    new_ingredient_name = ingredient_form.cleaned_data["new_ingredient"]
                    new_ingredient, created = Ingredient.objects.get_or_create(name=new_ingredient_name)
                    ingredient_form.instance.ingredient = new_ingredient  # ✅ Assign new ingredient

            ingredient_formset.save()
            return redirect("ledger:recipe_list")
        else:
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