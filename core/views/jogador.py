import logging

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template.defaultfilters import slugify

from django.views.generic import (
    ListView, FormView, DetailView, 
    FormView,TemplateView, CreateView, 
    UpdateView, DeleteView, View
)

from core.models import Jogador, Classe, Equipe, Quest

logger = logging.getLogger(__name__)


class JogadorListView(ListView):
    model = Jogador
    template_name = "jogador/list.html"
    ordering = ["name"]
    paginate_by = 5


class JogadorCreateView(CreateView):
    model = Jogador
    template_name = "jogador/create.html"
    fields = [
        "name", "jogador",
        "init_date", "end_date",
        "points", "description"
    ]


class JogadorDetailView(DetailView):
    model = Jogador
    template_name = "jogador/details.html"


class JogadorDeleteView(DeleteView):
    model = Jogador
    template_name = "jogador/delete.html"


class JogadorUpdateView(UpdateView):
    model = User
    template_name = 'jogador/update.html'
    success_url = 'core:jogador_details'
    fields = [
        'username', 'email',
        'first_name', 'last_name'
    ]

    def get_success_url(self):
        return reverse(
            self.success_url,
            kwargs=({
                'pk':self.get_object().pk
            })
        )
