from django import forms
from .models import Restaurant, MenuItem


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ['name', 'description', 'cuisine', 'address', 'image', 'avg_prep_time']


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'category', 'is_veg', 'image', 'is_available']
