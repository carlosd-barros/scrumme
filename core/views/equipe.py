import logging

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.defaultfilters import slugify

from django.views.generic import (
    ListView, FormView, DetailView, 
    FormView,TemplateView, CreateView, 
    UpdateView, DeleteView, View
)

from core.forms import EquipeCreateForm
from core.models import Jogador, Classe, Equipe, Quest

logger = logging.getLogger(__name__)


class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    template_name = "equipe/list.html"
    ordering = ["name"]
    paginate_by = 5
    permission_denied_message = (
        'Você não possui permissão de acesso.'
    )

    def get_queryset(self):
        queryset = super(EquipeListView, self).get_queryset()
        integrante = self.request.user.jogador
        queryset = queryset.filter(
            Q(lider=integrante) |
            Q(team__in=[integrante])
        )

        return queryset

class EquipeCreateView(LoginRequiredMixin, CreateView):
    model = Equipe
    form_class = EquipeCreateForm
    success_url = reverse_lazy('core:equipe_list')
    template_name = "equipe/create.html"

    def form_valid(self, form):
        if self.request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    self.request,
                    "Equipe criada com sucesso."
                )
            else:
                messages.error(
                    self.request,
                    'Ops, parece que algo deu errado.'
                )
                form = EquipeCreateForm()

        return super(
            EquipeCreateView, self).form_valid(form)


class EquipeDetailView(DetailView):
    model = Equipe
    template_name = "equipe/detail.html"


class EquipeDeleteView(DeleteView):
    model = Equipe
    template_name = "equipe/delete.html"


class EquipeUpdateView(UpdateView):
    model = Equipe
    template_name = "equipe/update.html"
    fields = [
        "name", "jogador",
        "init_date", "end_date",
        "points", "description"
    ]
