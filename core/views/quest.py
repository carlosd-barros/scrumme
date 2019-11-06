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


class QuestListView(ListView):
    model = Quest
    template_name = "quest/list.html"
    ordering = ["name"]
    paginate_by = 5


class QuestCreateView(CreateView):
    model = Quest
    template_name = "quest/create.html"
    fields = [
        "name", "jogador",
        "init_date", "end_date",
        "points", "description"
    ]


class QuestDetailView(DetailView):
    model = Quest
    template_name = "quest/detail.html"


class QuestDeleteView(DeleteView):
    model = Quest
    template_name = "quest/delete.html"


class QuestUpdateView(UpdateView):
    model = Quest
    template_name = "quest/update.html"
    fields = [
        "name", "jogador",
        "init_date", "end_date",
        "points", "description"
    ]
