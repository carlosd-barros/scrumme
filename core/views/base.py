import logging

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User

from django.views.generic import (
    ListView, FormView, DetailView, 
    FormView,TemplateView, CreateView, 
    UpdateView, DeleteView, View
)

from core.models import Jogador, Classe, Equipe, Quest

logger = logging.getLogger(__name__)


class DashboardView(TemplateView):
    template_name = 'core/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            jogador, created = Jogador.objects.get_or_create(
                user=request.user,
                defaults={
                    'user':request.user,
                    'name':(
                        f"{request.user.first_name} "
                        f"{request.user.last_name}"
                    )
                }
            )

            if jogador.name == '':
                jogador.name = jogador.user.username
                jogador.save()

        # else:
        #     messages.error(
        #         request,
        #         'É necessário estar logado para obter acesso.'
        #     )
        #     return HttpResponseRedirect(
        #         reverse('accounts:login')
        #     )

        return super(
            DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        player = None
        if self.request.user.is_authenticated:
            player = self.request.user.jogador

        context['equipes'] = Equipe.objects.filter(
            team__in=[player]
        )
        context['quests'] = Quest.objects.filter(
            responsaveis__in=[player]
        )

        return context


class NotFoundView(TemplateView):
    template_name = 'http_erros/404.html'
