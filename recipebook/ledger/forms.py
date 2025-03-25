from django import forms
from django.forms import inlineformset_factory
from .models import Recipe, RecipeImage, RecipeIngredient, Ingredient

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ["name"]


class RecipeImageForm(forms.ModelForm): 
    class Meta:
        model = RecipeImage
        fields = ["image", "description"]


class RecipeIngredientForm(forms.ModelForm):
    new_ingredient = forms.CharField(
        required=False,
        label="Or create a new ingredient"
    )


    class Meta:
        model = RecipeIngredient
        fields = ["ingredient", "quantity"]

    def clean(self):
        cleaned_data = super().clean()
        ingredient = cleaned_data.get("ingredient")
        new_ingredient = cleaned_data.get("new_ingredient")

        if not ingredient and not new_ingredient:
            raise forms.ValidationError("Please choose an existing ingredient or enter a new one.")

        if ingredient and new_ingredient:
            raise forms.ValidationError("Choose an existing ingredient OR enter a new one, not both.")

        return cleaned_data

RecipeIngredientFormSet = inlineformset_factory(
    Recipe, RecipeIngredient, form=RecipeIngredientForm, extra=1, can_delete=True
)