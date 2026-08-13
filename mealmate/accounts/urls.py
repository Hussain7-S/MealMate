from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.MealMateLoginView.as_view(), name='login'),
    path('logout/', views.MealMateLogoutView.as_view(), name='logout'),
]
