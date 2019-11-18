import logging

from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
from django.http.response import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView, FormView, DetailView, 
    FormView,TemplateView, CreateView, 
    UpdateView, DeleteView, View
)

from core.models import Jogador, Classe, Equipe, Quest, Projeto

from core.forms.create import ProjetoCreateForm, QuestCreateForm

logger = logging.getLogger(__name__)



class ProjetotListView(ListView):
    model = Projeto
    form_class = ProjetoCreateForm
    template_name = 'projeto/list.html'

    def get_queryset(self):
        jogador = self.request.user.jogador

        equipes = Equipe.objects.filter(
            Q(lider=jogador) | Q(team__in=[jogador])
        ).distinct()

        return super().get_queryset().filter(
            Q(responsavel=jogador) | Q(equipe__in=equipes)
        ).distinct()
    

class ProjetoDetailView(DetailView):
    model = Projeto
    template_name = 'projeto/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # jogador = self.request.user.jogador

        context["quests"] = Quest.objects.filter(
            project=self.get_object()
        ).distinct()

        logger.debug(f"quests aqui: {context.get('quests')}")

        return context
    
