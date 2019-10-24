# import json
import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse

from django.views.generic import ListView, DetailView
from django.views.generic.base import View, TemplateView


from accounts.models import Pessoa

logger = logging.getLogger(__name__)

class DashboardView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        pessoa = None

        if self.request.user.is_authenticated:
            pessoa = Pessoa.objects.get_or_create(
                user=self.request.user,
                defaults={
                    'user':self.request.user,
                    'name': self.request.user.first_name
                }
            )[0]

        kwargs.update({
            'pessoa': pessoa
        })

        return super(
            DashboardView, self).get_context_data(**kwargs)

class NotFoundView(TemplateView):
    template_name = '404.html'