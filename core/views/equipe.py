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
from core.forms import EquipeCreateForm
from core.models import Jogador, Classe, Equipe, Quest

logger = logging.getLogger(__name__)


class EquipeListView(ListView):
    model = Equipe
    template_name = "equipe/list.html"
    ordering = ["name"]
    paginated_by = 5


class EquipeCreateView(FormView):
    form_class = EquipeCreateForm
    template_name = "equipe/create.html"


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
