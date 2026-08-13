from django.urls import path
from . import views

app_name = 'restaurants'

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/new/', views.restaurant_create, name='restaurant_create'),
    path('dashboard/<int:pk>/menu/new/', views.menu_item_create, name='menu_item_create'),
    path('<int:pk>/', views.restaurant_detail, name='detail'),
]
