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

    @transaction.atomic
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            name = f"{request.user.first_name} {request.user.last_name}"

            jogador, created = Jogador.objects.get_or_create(
                user=request.user,
                defaults={
                    'user':request.user,
                    'name':name if len(name) > 1 else request.user.username.upper()
                }
            )

        return super(
            DashboardView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        jogador = None

        if self.request.user.is_authenticated:
            jogador = self.request.user.jogador

        equipes = Equipe.objects.filter(
            (
                Q(lider=jogador) | Q(team__in=[jogador])
            ) &
            Q(active=True)
        ).distinct()

        context['equipes'] = equipes

        context['quests'] = Quest.objects.filter(
            (
                Q(responsaveis__in=[jogador]) | Q(equipe__in=equipes)
            ) &
            Q(open=True)
        ).distinct()

        return context


class NotFoundView(TemplateView):
    template_name = 'http_erros/404.html'
