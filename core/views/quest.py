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

    def get_queryset(self):
        return super().get_queryset().filter(
            responsaveis__in=[self.request.user.jogador]
        ).distinct()


class QuestCreateView(CreateView):
    model = Quest
    form_class = QuestCreateForm
    template_name = "quest/create.html"
    success_url = reverse_lazy('core:quest_list')

    @transaction.atomic
    def form_valid(self, form):
        if self.request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    self.request,
                    "Quest criada com sucesso."
                )
            else:
                messages.error(
                    self.request,
                    'Ops, parece que algo deu errado.'
                )
                form = form(self.request.POST)

        return super(
            QuestCreateView, self).form_valid(form)


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

