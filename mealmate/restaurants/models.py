from django.conf import settings
from django.db import models


class Restaurant(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restaurants')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    cuisine = models.CharField(max_length=100, blank=True, help_text="e.g. Indian, Chinese, Italian")
    address = models.CharField(max_length=255)
    image = models.ImageField(upload_to='restaurants/', blank=True, null=True)
    is_open = models.BooleanField(default=True)
    avg_prep_time = models.PositiveIntegerField(default=30, help_text="Minutes")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def average_rating(self):
        agg = self.reviews.aggregate(models.Avg('rating'))
        val = agg['rating__avg']
        return round(val, 1) if val else 0.0


class MenuItem(models.Model):
    CATEGORY_CHOICES = (
        ('starter', 'Starter'),
        ('main', 'Main Course'),
        ('dessert', 'Dessert'),
        ('beverage', 'Beverage'),
    )
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='main')
    is_veg = models.BooleanField(default=True)
    image = models.ImageField(upload_to='menu/', blank=True, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rating}★ - {self.restaurant.name}"
