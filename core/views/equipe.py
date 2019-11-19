import logging
from random import randint

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
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

from core.forms.create import EquipeCreateForm, QuestCreateForm
from core.models import Jogador, Classe, Equipe, Quest
from core.choices import QuestLevel

logger = logging.getLogger(__name__)


class EquipeListView(LoginRequiredMixin, ListView):
    model = Equipe
    template_name = "equipe/list.html"
    ordering = ["-created"]

    def get_queryset(self):
        queryset = super(EquipeListView, self).get_queryset()
        jogador = self.request.user.jogador

        queryset = queryset.filter(
            Q(lider=jogador) | Q(team__in=[jogador])
        ).distinct()

        return queryset


class EquipeCreateView(LoginRequiredMixin, CreateView):
    model = Equipe
    form_class = EquipeCreateForm
    success_url = reverse_lazy('core:equipe_list')
    template_name = "equipe/create.html"

    @transaction.atomic
    def form_valid(self, form):
        if self.request.method == 'POST':
            if form.is_valid():
                form.save()
                messages.success(
                    self.request,
                    'Equipe criada com sucesso.'
                )
            else:
                messages.error(
                    self.request,
                    'Ops, parece que algo deu errado.'
                )
                form = EquipeCreateForm()

        return super(
            EquipeCreateView, self).form_valid(form)


class EquipeDetailView(LoginRequiredMixin, DetailView):
    model = Equipe
    template_name = "equipe/detail.html"

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form':QuestCreateForm,
        })

        return super(
            EquipeDetailView, self).get_context_data(**kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = QuestCreateForm(request.POST)

        if form.is_valid:
            quest = form.save(commit=False)
            level = quest.level

            if level == QuestLevel.BAIXO.code:
                quest.points = randint(1,5)

            elif level == QuestLevel.MEDIO.code:
                quest.points = randint(4,8)

            elif level == QuestLevel.ALTO.code:
                quest.points = randint(7,11)

            quest.equipe = self.get_object()


            quest.save()

            messages.success(
                request,
                'Quest criada com sucesso. Agora defina os responsáveis.'
            )

            return HttpResponseRedirect(
                reverse('core:quest_confirm', kwargs={'pk':quest.pk})
            )

        messages.error(
            request, 'Ops, verifique os dados do formulário.'
        )

        return HttpResponseRedirect(
            reverse('core:equipe_detail', kwargs={'pk':self.get_object().pk})
        )


class EquipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipe
    success_url = reverse_lazy('core:equipe_list')
    template_name = "equipe/delete.html"

class EquipeUpdateView(LoginRequiredMixin, UpdateView):
    model = Equipe
    template_name = "equipe/update.html"
    success_url = 'core:equipe_detail'
    fields = [
        'lider', 'team'
    ]

    def test_func(self):
        equipe = self.get_object()
        if self.request.object == equipe:
            return True
        return False

    def get_success_url(self):
        return reverse(
            self.success_url,
            kwargs={'pk':self.get_object().pk}
        )

