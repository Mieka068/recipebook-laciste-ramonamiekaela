from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .models import Recipe, RecipeImage
from .forms import RecipeForm, RecipeImageForm

def recipe_list(request):
    recipes = Recipe.objects.all()

    return render(request, "ledger/recipe_list.html", {"recipes":recipes})

@login_required
def recipe_detail(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    return render(request, "ledger/recipe_detail.html", {"recipe": recipe})


class AddRecipeView(LoginRequiredMixin, CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = "ledger/add_recipe.html"  
    success_url = reverse_lazy("ledger:recipe_list")  

    def form_valid(self, form):
        form.instance.author = self.request.user  
        return super().form_valid(form)


class AddImageView(CreateView):
    model = RecipeImage
    form_class = RecipeImageForm
    template_name = "ledger/add_image.html"

    def form_valid(self, form):
        form.instance.recipe = get_object_or_404(Recipe, id=self.kwargs["recipe_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ledger:recipe_detail", kwargs={"recipe_id": self.kwargs["recipe_id"]})
    
    