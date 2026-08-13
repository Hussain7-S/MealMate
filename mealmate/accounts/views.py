from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from .forms import SignUpForm


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response

    def get_success_url(self):
        if self.object.is_owner():
            return '/restaurants/dashboard/'
        return '/'


class MealMateLoginView(LoginView):
    template_name = 'accounts/login.html'


class MealMateLogoutView(LogoutView):
    next_page = '/'
