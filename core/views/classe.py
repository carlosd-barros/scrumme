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


class ClasseListView(ListView):
    model = Classe
    template_name = "classe/list.html"
    ordering = ["name"]
    paginated_by = 5


class ClasseCreateView(CreateView):
    model = Classe
    template_name = "classe/create.html"
    fields = [
        "name", "min_points", "max_points"
    ]


class ClasseDetailView(DetailView):
    model = Classe
    template_name = "classe/detail.html"


class ClasseDeleteView(DeleteView):
    model = Classe
    template_name = "classe/delete.html"


class ClasseUpdateView(UpdateView):
    model = Classe
    template_name = "classe/update.html"
    fields = [
        "name", "min_points", "max_points"
    ]
