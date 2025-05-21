from django.urls import path
from .views import home, RecipeListView, RecipeDetailView, search, add_recipe, about

app_name = "recipes"

urlpatterns = [
    path("", home, name="home"),
    path("collection", RecipeListView.as_view(), name="list"),
    path("collection/<pk>", RecipeDetailView.as_view(), name="detail"),
    path("search", search, name="search"),
    path("add_recipe", add_recipe, name="add_recipe"),
    path("about", about, name="about"),
]