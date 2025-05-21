from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
import pandas as pd
from .models import Recipe
from .forms import RecipesSearchForm, AddRecipeForm
from .utils import get_chart


# Create your views here.
# FBV "home"
def home(request):
    return render(request, "recipes/recipes_home.html")

# FBV "about"
def about(request):
    return render(request, "recipes/about.html")

# CBV "RecipeList", protected
class RecipeListView(LoginRequiredMixin, ListView):
    model = Recipe

    template_name = "recipes/collection.html"

# CBV "RecipeDetail", protected
class RecipeDetailView(LoginRequiredMixin, DetailView):
    model = Recipe

    template_name = "recipes/detail.html"

# FBV "search", protected
@login_required
def search(request):
    # adds an instance of RecipesSearchForm
    form = RecipesSearchForm(request.POST or None)

    # Initializes dataframe to None
    recipes_df = None

    bar_chart = None
    pie_chart = None
    line_chart = None

    if request.method == "POST" and form.is_valid():
        # Retrieves the search criteria from the form
        search_by = form.cleaned_data.get("search_by")
        search_term = form.cleaned_data.get("search_term")
        ingredients = form.cleaned_data.get("ingredients")
        difficulty = form.cleaned_data.get("difficulty")

        # Filters the queryset based on the form input
        qs = Recipe.objects.all()

        if search_by == "name" and search_term:
            qs = qs.filter(name__icontains=search_term)
        elif search_by == "ingredients" and ingredients is not None:
            qs = qs.filter(ingredients=ingredients)
        elif search_by == "difficulty" and difficulty:
            qs = [recipe for recipe in qs if recipe.difficulty == difficulty]

        # Checks if the queryset is not empty
        if qs:
            # Converts list to pandas dataframe, else converts queryset to pandas DataFrame
            if isinstance(qs, list):
                recipes_df = pd.DataFrame([recipe.__dict__ for recipe in qs])
            else:
                recipes_df = pd.DataFrame(qs.values())

            recipes_df.index += 1

            # Retrieves each Recipe object using its id, then calls get_absolute_url() on it to generate the link
            def format_recipe_name_table(row):
                recipe = Recipe.objects.get(id=row["id"])
                return f"<a href='{recipe.get_absolute_url()}'>{row['name']}</a>"
            
            def format_recipe_name_chart(row):
                return row["name"]

            recipes_df["name_table"] = recipes_df.apply(format_recipe_name_table, axis=1)
            recipes_df["name_chart"] = recipes_df.apply(format_recipe_name_chart, axis=1)

            # Calculates difficulty and number of ingredients for each recipe
            recipes_df["difficulty"] = [recipe.difficulty for recipe in qs]
            recipes_df["number_of_ingredients"] = recipes_df["ingredients"].apply(lambda x: len(x.split(", ")))

            # Generate charts
            bar_chart = get_chart("#1", recipes_df, labels=recipes_df["name_chart"].values)
            pie_chart = get_chart("#2", recipes_df, labels=recipes_df["difficulty"].values)
            line_chart = get_chart("#3", recipes_df, labels=recipes_df["name_chart"].values)

            recipes_df = recipes_df[["name_table", "cooking_time", "difficulty"]]
            recipes_df = recipes_df.rename(columns={"name_table": "Name"})
            recipes_df = recipes_df.rename(columns={"cooking_time": "Cooking Time (in minutes)"})
            recipes_df.columns = recipes_df.columns.str.capitalize()

            # Convert DataFrame to HTML for display
            recipes_df = recipes_df.to_html(escape=False)


    # Prepares data to send from view to template
    context = {
        "form": form,
        "recipes_df": recipes_df,
        "bar_chart": bar_chart,
        "pie_chart": pie_chart,
        "line_chart": line_chart,
    }

    # Loads page using "context" information
    return render(request, "recipes/search.html", context)

# FBV "add_recipe"
@login_required
def add_recipe(request):

    if request.method == "POST":
        # Creates an instance of AddRecipeForm with the submitted data and files
        add_recipe_form = AddRecipeForm(request.POST, request.FILES)

        # Validates form data
        if add_recipe_form.is_valid():
            # Saves form data to database
            add_recipe_form.save()

            # Adds a success message to display to user
            messages.success(request, "Recipe added successfully.")

            # Redirects user to "add_recipe" page
            return redirect("recipes:list")
    else:
        # Creates an empty form instance if request method is not POST
        add_recipe_form = AddRecipeForm()

    # Prepares data to send from view to template
    context = {
        "add_recipe_form": add_recipe_form
    }

    # Loads page using "context" information
    return render(request, "recipes/add_recipe.html", context)