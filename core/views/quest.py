import logging

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render, redirect
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

from core.forms import QuestCreateForm

logger = logging.getLogger(__name__)


class QuestListView(ListView):
    model = Quest
    template_name = "quest/list.html"
    ordering = ["-created"]
    paginate_by = 5


class QuestCreateView(CreateView):
    model = Quest
    form_class = QuestCreateForm
    template_name = "quest/create.html"
    success_url = reverse_lazy('core:quest_list')

    def form_valid(self, form):
        quest = form.save(commit=False)
        quest.save()
        return redirect('core:dashboard')


class QuestDetailView(DetailView):
    model = Quest
    template_name = "quest/detail.html"


class QuestDeleteView(DeleteView):
    model = Quest
    template_name = "quest/delete.html"
    success_url = reverse_lazy('core:quest_list')


class QuestUpdateView(UpdateView):
    model = Quest
    form_class = QuestCreateForm
    template_name = "quest/update.html"
    success_url = reverse_lazy('core:quest_list')

