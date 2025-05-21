from django.db import models
from django.shortcuts import reverse

# Create your models here.
class Recipe(models.Model):
    # Class attributes
    name = models.CharField(max_length=50)
    ingredients = models.CharField(
        max_length=255,
        help_text='Enter ingredients, separated by a comma.'
    )
    cooking_time = models.IntegerField(help_text='Enter cooking time (minutes).')
    pic = models.ImageField(upload_to="recipes", default="no_picture.jpg")


    # Determines recipe difficulty
    @property
    def difficulty(self):
        ingredients = self.ingredients.split(", ")

        if self.cooking_time < 10 and len(ingredients) < 4:
            return 'Easy'
        elif self.cooking_time < 10 and len(ingredients) >= 4:
            return 'Medium'
        elif self.cooking_time >= 10 and len(ingredients) < 4:
            return 'Intermediate'
        elif self.cooking_time >= 10 and len(ingredients) >= 4:
            return 'Hard'
        return 'Unknown'

    # String representation
    def __str__(self):
        return str(self.name)
    
    # Creates the primary key of the recipe objects to become clickable
    def get_absolute_url(self):
        return reverse ('recipes:detail', kwargs={'pk': self.pk})
    
    # Split the ingredients field by commas and return as a list.
    def return_ingredients_as_list(self):
        return self.ingredients.split(",") # Split the ingredients field by commas and return as a list.