from django.urls import path
from . import views

app_name = 'aibuddy'

urlpatterns = [
    path('chat/', views.chat, name='chat'),
]
