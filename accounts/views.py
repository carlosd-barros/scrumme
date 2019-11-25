import logging

from django.urls import reverse
from django.db import transaction
from django.shortcuts import render
from django.urls.base import reverse_lazy

from django.views.generic import FormView, View
from django.contrib import messages

from .forms import AuthRegisterForm


logger = logging.getLogger(__name__)

class AuthRegisterView(FormView):
    form_class = AuthRegisterForm
    template_name = 'auth/register.html'
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        if self.request.method == "POST":
            form = AuthRegisterForm(self.request.POST)
            if form.is_valid():
                form.save()
                first_name = form.cleaned_data.get('first_name').capitalize()
                messages.success(
                    self.request, 
                    f'{first_name}, sua conta foi criada com sucesso!'
                )
            else:
                return self.form_invalid(form)
        else:
            form = AuthRegisterForm()

        return super(
            AuthRegisterView, self).form_valid(form)

