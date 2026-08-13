from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, widget=forms.RadioSelect)
    email = forms.EmailField(required=True)
    phone = forms.CharField(required=False, max_length=15)
    address = forms.CharField(required=False, max_length=255)

    class Meta:
        model = User
        fields = ('username', 'email', 'role', 'phone', 'address', 'password1', 'password2')
