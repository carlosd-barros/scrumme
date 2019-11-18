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

from core.models import Jogador, Classe, Equipe, Quest

from core.forms.create import QuestCreateForm
from core.forms.update import QuestUpdateForm

logger = logging.getLogger(__name__)


class QuestListView(LoginRequiredMixin, ListView):
    model = Quest
    template_name = "quest/list.html"
    ordering = ["-created"]

    def get_queryset(self):
        return super().get_queryset().filter(
            responsaveis__in=[self.request.user.jogador]
        ).distinct()


class QuestCreateView(LoginRequiredMixin, CreateView):
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


class QuestDetailView(LoginRequiredMixin, DetailView):
    model = Quest
    template_name = "quest/detail.html"


class QuestComplete(View):
    quest_id = None
    success_url = reverse_lazy('core:quest_list')
    template_name = 'quest/detail.html'

    def dispatch(self, request, *args, **kwargs):
        self.quest_id = kwargs.get('pk')

        return super(
            QuestComplete, self).dispatch(request, *args, **kwargs)

    def post(self, request, pk):
        quest = get_object_or_404(Quest, pk=pk)
        jogadores = quest.responsaveis

        for jogador in jogadores.all():
            jogador.points += quest.points
            jogador.save()

        quest.open = False
        quest.save()

        return HttpResponseRedirect(self.success_url)

    # def get_success_url(self):
    #     return reverse(
    #         self.success_url, kwargs={'pk':self.quest_id}
    #     )


class QuestDeleteView(LoginRequiredMixin, DeleteView):
    model = Quest
    template_name = "quest/delete.html"
    success_url = reverse_lazy('core:quest_list')


class QuestUpdateView(LoginRequiredMixin, UpdateView):
    model = Quest
    form_class = QuestUpdateForm
    template_name = "quest/update.html"
    success_url = 'core:quest_detail'

    def form_valid(self, form):
        if self.request.method == 'POST':
            if form.is_valid:
                form.save()
                messages.success(
                    self.request,
                    'Quest editada com sucesso.'
                )

                return HttpResponseRedirect(
                    self.get_success_url()
                )

            else:
                messages.error(
                    self.request, 'Ops, verifique os dados informados.'
                )
                return render(
                    self.request, self.template_name, self.get_context_data()
                )

        return reverse_lazy('core:quest_list')

    def get_success_url(self):
        return reverse(
            self.success_url, kwargs={'pk':self.get_object().pk}
        )

