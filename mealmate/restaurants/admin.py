from django.contrib import admin
from .models import Restaurant, MenuItem, Review


class MenuItemInline(admin.TabularInline):
    model = MenuItem
    extra = 1


@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'cuisine', 'is_open', 'avg_prep_time')
    inlines = [MenuItemInline]


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'price', 'category', 'is_available')
    list_filter = ('category', 'is_veg', 'is_available')


admin.site.register(Review)
