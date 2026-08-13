from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .models import Restaurant, MenuItem
from .forms import RestaurantForm, MenuItemForm


def home(request):
    query = request.GET.get('q', '')
    cuisine = request.GET.get('cuisine', '')
    restaurants = Restaurant.objects.filter(is_open=True)
    if query:
        restaurants = restaurants.filter(Q(name__icontains=query) | Q(cuisine__icontains=query))
    if cuisine:
        restaurants = restaurants.filter(cuisine__iexact=cuisine)
    cuisines = Restaurant.objects.values_list('cuisine', flat=True).distinct()
    return render(request, 'restaurants/home.html', {
        'restaurants': restaurants,
        'cuisines': [c for c in cuisines if c],
        'query': query,
    })


def restaurant_detail(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk)
    items = restaurant.menu_items.filter(is_available=True)
    category = request.GET.get('category')
    if category:
        items = items.filter(category=category)
    return render(request, 'restaurants/detail.html', {
        'restaurant': restaurant,
        'items': items,
        'categories': MenuItem.CATEGORY_CHOICES,
    })


@login_required
def dashboard(request):
    if not request.user.is_owner():
        return redirect('restaurants:home')
    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'restaurants/dashboard.html', {'restaurants': restaurants})


@login_required
def restaurant_create(request):
    if not request.user.is_owner():
        return redirect('restaurants:home')
    if request.method == 'POST':
        form = RestaurantForm(request.POST, request.FILES)
        if form.is_valid():
            restaurant = form.save(commit=False)
            restaurant.owner = request.user
            restaurant.save()
            return redirect('restaurants:dashboard')
    else:
        form = RestaurantForm()
    return render(request, 'restaurants/restaurant_form.html', {'form': form})


@login_required
def menu_item_create(request, pk):
    restaurant = get_object_or_404(Restaurant, pk=pk, owner=request.user)
    if request.method == 'POST':
        form = MenuItemForm(request.POST, request.FILES)
        if form.is_valid():
            item = form.save(commit=False)
            item.restaurant = restaurant
            item.save()
            return redirect('restaurants:dashboard')
    else:
        form = MenuItemForm()
    return render(request, 'restaurants/menu_item_form.html', {'form': form, 'restaurant': restaurant})
