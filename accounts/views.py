from django.shortcuts import render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    AuthenticationForm
)
from django.contrib import messages

class RegisterView(FormView):
    form_class = UserCreationForm
    template_name = 'auth/register.html'

    def form_valid(self, form):
        if self.request.method == "POST":
            form = UserCreationForm(self.request.POST)
            if form.is_valid():
                username = self.request.user.username
        else:
            form = UserCreationForm()

        return super(
            RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('auth:login')

class AuthLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'auth/login.html'
    sucess_url = 'core:dashboard'

    def form_valid(self, form):
        if self.request.method == "POST":
            form = AuthenticationForm(self.request.POST)
        else:
            form = AuthenticationForm()

        return super(
            AuthLoginView, self).form_valid(form)

    def get_success_url(self):
        return reverse('core:dashboard')

class AuthLogout(FormView):
    pass

class AuthRegister(FormView):
    pass
