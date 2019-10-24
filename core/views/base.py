# import json
import logging

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.http.response import HttpResponse

from django.views.generic import ListView, DetailView
from django.views.generic.base import View, TemplateView


from accounts.models import Jogador

logger = logging.getLogger(__name__)

class DashboardView(TemplateView):
    template_name = 'core/index.html'

    def get_context_data(self, **kwargs):
        player = None

        if self.request.user.is_authenticated:
            player = Jogador.objects.get_or_create(
                user=self.request.user,
                defaults={
                    'user':self.request.user,
                    'name': self.request.user.first_name
                }
            )[0]

        kwargs.update({
            'pessoa': player
        })

        return super(
            DashboardView, self).get_context_data(**kwargs)

class NotFoundView(TemplateView):
    template_name = '404.html'