from django.db import models
from django.conf import settings

class Restaurant(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255, blank=True)
    cuisine_type = models.CharField(max_length=100, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='categories')

    def __str__(self):
        return self.name

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=200)
    ingredients = models.TextField(help_text="Comma-separated list of ingredients.")
    allergens = models.TextField(blank=True, help_text="Comma-separated list of allergens (e.g., 'nuts,dairy').")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="menu_items")
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name} ({self.category if self.category else 'No Category'})"
