from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Recipe
from .forms import RecipesSearchForm, AddRecipeForm

class RecipeModelTest(TestCase):
    def setUpTestData():
        # Sets up non-modified objects used by all test methods
        Recipe.objects.create(
            name = 'Herbal Tea',
            ingredients = 'Herbal Tea Leaves, Honey, Hot Water',
            cooking_time = 5,
        )

    # ------------------------- Name ------------------------- 
    def test_recipe_name(self):
        # Gets recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Gets metadata for "name"
        field_label = recipe._meta.get_field('name').verbose_name

        # Compares value to expected result
        self.assertEqual(field_label, 'name')

    def test_recipe_name_max_length(self):
        # Gets recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Gets metadata for "name"
        max_length = recipe._meta.get_field('name').max_length

        # Compares value to expected result
        self.assertEqual(max_length, 50)

    # ------------------------- Ingredients ------------------------- #
    def test_ingredients_max_length(self):
        # Gets recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Gets metadata for "ingredients"
        max_length = recipe._meta.get_field('ingredients').max_length

        # Compares value to expected result
        self.assertEqual(max_length, 255)

    # ------------------------- Cooking Time ------------------------- #
    def test_cooking_time_value(self):
        # Gets recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Gets the value of "cooking_time"
        cooking_time_value = recipe.cooking_time

        # Compares value to expected result
        self.assertIsInstance(cooking_time_value, int)

    # ------------------------- Difficulty ------------------------- #
    def test_difficulty_calulation(self):
        # Gets recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Compares value to expected result
        self.assertEqual(recipe.difficulty, 'Easy')

        # ------------------------- URL ------------------------- #
    # Defines test for getting the absolute URL of a recipe object
    def test_get_absolute_url(self):
        # Gets a recipe object to test
        recipe = Recipe.objects.get(id=1)

        # Compares value to expected result
        self.assertEqual(recipe.get_absolute_url(), "/collection/1")

class RecipeFormTest(TestCase):
    # ------------------------- Search ------------------------- #
    def test_search_form_valid_data(self):
        # Creates a RecipesSearchForm instance with valid data
        form = RecipesSearchForm(data={
            "search_by": "name",
            "search_term": "Test Recipe",
            "ingredients": "",
            "difficulty": "",
        })

        # Checks if form is valid
        self.assertTrue(form.is_valid())

    def test_search_form_invalid_data(self):
        # Creates a RecipesSearchForm instance with empty data
        form = RecipesSearchForm(data={})

        # Checks if form is invalid
        self.assertFalse(form.is_valid())

    def test_search_form_field_labels(self):
        # Creates a RecipesSearchForm instance
        form = RecipesSearchForm()

        # Checks if "search_by" field label is "Search by"
        self.assertEqual(form.fields["search_by"].label, "Search by")

        # Checks if "search_term" field label is "Search term"
        self.assertEqual(form.fields["search_term"].label, "Search term")

        # Checks if "ingredients" field label is "Ingredient"
        self.assertEqual(form.fields["ingredients"].label, "Ingredients")

        # Checks if "difficulty" field label is "Difficulty"
        self.assertEqual(form.fields["difficulty"].label, "Difficulty")


class RecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creates test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

        # Creates test recipes
        cls.recipe1 = Recipe.objects.create(name="Recipe 1", ingredients="ingredient1, ingredient2", cooking_time=10)
        cls.recipe2 = Recipe.objects.create(name="Recipe 2", ingredients="ingredient1, ingredient2", cooking_time=20)

    def setUp(self):
        # Initializes test client
        self.client = Client()

    def test_recipe_list_view_login_required(self):
        # Sends GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        # Checks if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:list')}")

    def test_recipe_list_view(self):
        # Logs test user in
        self.client.login(username="testuser", password="12345")

        # Sends GET request to recipe list view
        response = self.client.get(reverse("recipes:list"))

        # Checks if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if correct template is used
        self.assertTemplateUsed(response, "recipes/collection.html")

        # Checks if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

        # Checks if response contains the second recipe name
        self.assertContains(response, "Recipe 2")

    def test_recipe_detail_view_login_required(self):
        # Sends GET request to recipe detail view for the first recipe
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe1.pk}))

        # Checks if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:detail', kwargs={'pk': self.recipe1.pk})}")

    def test_recipe_detail_view(self):
        # Logs test user in
        self.client.login(username="testuser", password="12345")

        # Sends GET request to recipe detail view for the first recipe
        response = self.client.get(reverse("recipes:detail", kwargs={"pk": self.recipe1.pk}))

        # Checks if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if correct template is used
        self.assertTemplateUsed(response, "recipes/detail.html")

        # Checks if response contains the first recipe name
        self.assertContains(response, "Recipe 1")

    def test_search_view_login_required(self):
        # Sends GET request to search view
        response = self.client.get(reverse("recipes:search"))

        # Checks if response redirects to login page with the next parameter set to requested URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:search')}")

    def test_search_view(self):
        # Logs test user in
        self.client.login(username="testuser", password="12345")

        # Sends POST request to search view with valid data
        response = self.client.post(reverse("recipes:search"), data={
            "search_by": "name",
            "search_term": "Recipe 1",
            "ingredients": "",
            "difficulty": "",
        })

        # Checks if response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Checks if correct template is used
        self.assertTemplateUsed(response, "recipes/search.html")

        # Checks if response contains the first recipe name
        self.assertContains(response, "Recipe 1")


class RecipeFormTest(TestCase):
    # Test form validation with valid data
    def test_add_recipe_form_valid_data(self):
        form = AddRecipeForm(data={
            "name": "Test Recipe",
            "ingredients": "Test Ingredients",
            "cooking_time": 30,
            "pic": None     # Assuming no file for simplicity
        })

        # Form should be valid
        self.assertTrue(form.is_valid())  

    # Test form validation with no data
    def test_add_recipe_form_no_data(self):
        form = AddRecipeForm(data={})

        # Form should be invalid
        self.assertFalse(form.is_valid())

        # Should have errors for all required fields
        self.assertEqual(len(form.errors), 3)


class AddRecipeViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Creates a test user
        cls.user = User.objects.create_user(username="testuser", password="12345")

    def setUp(self):
        # Creates a test client and log in the user
        self.client = Client()
        self.client.login(username="testuser", password="12345")

    # Test GET request to add_recipe view
    def test_add_recipe_view_get(self):
        response = self.client.get(reverse("recipes:add_recipe"))
        
        # Status code should be 200
        self.assertEqual(response.status_code, 200)

        # Should use the correct template
        self.assertTemplateUsed(response, "recipes/add_recipe.html")

        # Context should have AddRecipeForm
        self.assertIsInstance(response.context["add_recipe_form"], AddRecipeForm)

    # Test POST request with valid data to add_recipe view
    def test_add_recipe_view_post_valid_data(self):
        data = {
            "name": "Test Recipe",
            "ingredients": "Test Ingredients",
            "cooking_time": 30,
            "pic": ""  # Assuming no file for simplicity
        }

        response = self.client.post(reverse("recipes:add_recipe"), data)

        # Should redirect after successful form submission
        self.assertEqual(response.status_code, 302)
        
        # Should redirect to the recipe list view
        self.assertRedirects(response, reverse("recipes:list"))
        
        # One recipe should be created
        self.assertEqual(Recipe.objects.count(), 1)

        # Check for success message
        messages = list(get_messages(response.wsgi_request))

        # There should be one message
        self.assertEqual(len(messages), 1)

        # Message content should be correct
        self.assertEqual(str(messages[0]), "Recipe added successfully.")

    # Tests POST request with invalid data to add_recipe view
    def test_add_recipe_view_post_invalid_data(self):
        data = {}

        response = self.client.post(reverse("recipes:add_recipe"), data)

        # Should return 200 status code
        self.assertEqual(response.status_code, 200)

        # Should use the correct template
        self.assertTemplateUsed(response, "recipes/add_recipe.html")

        # Form should be invalid
        self.assertFalse(response.context["add_recipe_form"].is_valid())  

    # Tests that add_recipe view requires login
    def test_add_recipe_view_login_required(self):
        # Log out the test user
        self.client.logout()

        response = self.client.get(reverse("recipes:add_recipe"))

        # Should redirect to login page with next parameter set to add_recipe URL
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('recipes:add_recipe')}")