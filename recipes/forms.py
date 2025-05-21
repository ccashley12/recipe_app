from django import forms
from .models import Recipe

SEARCH_CHOICES = [
    ("name", "Recipe Name"),
    ("ingredients", "Ingredients"),
    ("difficulty", "Difficulty"),
]

# CBV "RecipesSearchForm"
class RecipesSearchForm(forms.Form):
    search_by = forms.ChoiceField(choices=SEARCH_CHOICES, required=True, label="Search by")
    search_term = forms.CharField(max_length=100, required=False, label="Search term")
    ingredients = forms.CharField(max_length=100, required=False, label="Ingredients")
    difficulty = forms.ChoiceField(
        choices=[
            ("Easy", "Easy"),
            ("Medium", "Medium"),
            ("Intermediate", "Intermediate"),
            ("Hard", "Hard"),
        ],
        required=False,
        label="Difficulty"
    )

# CBV "AddRecipeForm"
class AddRecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "name",
            "ingredients",
            "cooking_time",
            "pic"
        ]