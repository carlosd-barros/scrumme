from django.shortcuts import render
from django.urls import reverse
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
                messages.success(
                    self.request, f'{username}, sua conta foi criada com sucesso!')
        else:
            form = UserCreationForm()

        return super(
            RegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse('biblioteca:home')

class AuthLoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'auth/login'

class AuthLogout(FormView):
    pass

class AuthRegister(FormView):
    pass