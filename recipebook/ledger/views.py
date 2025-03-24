from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.forms import inlineformset_factory
from .models import Recipe, RecipeImage, RecipeIngredient
from .forms import RecipeForm, RecipeImageForm, RecipeIngredientFormSet

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context["formset"] = RecipeIngredientFormSet(self.request.POST)
        else:
            context["formset"] = RecipeIngredientFormSet()
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user  
        self.object = form.save()  

        # Process ingredient formset
        formset = RecipeIngredientFormSet(self.request.POST, instance=self.object)
        if formset.is_valid():
            formset.save()

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("ledger:recipe_detail", kwargs={"recipe_id": self.object.id})



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
    
    