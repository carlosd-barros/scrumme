from django.shortcuts import render
from django.urls import reverse
from django.urls.base import reverse_lazy
from django.views.generic import FormView, View
from django.contrib import messages
from django.contrib.auth.forms import (
    UserCreationForm, 
    UserChangeForm, 
    AuthenticationForm
)
from .forms import AuthRegisterForm
from django.contrib import messages

import logging

logger = logging.getLogger(__name__)

class AuthRegisterView(FormView):
    form_class = AuthRegisterForm
    template_name = 'auth/register.html'
    sucess_url = 'auth:login'

    def form_valid(self, form):
        if self.request.method == "POST":
            logger.debug('tá funfando')
            form = AuthRegisterForm(self.request.POST)
            if form.is_valid():
                form.save()
                first_name = form.cleaned_data.get('first_name').capitalize()
                messages.success(
                    self.request, 
                    f'{first_name}, sua conta foi criada com sucesso!'
                )
        else:
            logger.debug('deu ruim man')
            form = UserCreationForm()

        return super(
            AuthRegisterView, self).form_valid(form)

    def get_success_url(self):
        return reverse(self.sucess_url)

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
