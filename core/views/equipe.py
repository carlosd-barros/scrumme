import logging

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http.response import (
    Http404,
    HttpResponse,
    HttpResponseRedirect,
    HttpResponseForbidden,
)

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic.base import RedirectView, TemplateView, View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import (
    CreateView, DeleteView, FormView, UpdateView,
)

from core.forms.create import (
    QuestCreateForm,
    EquipeCreateForm,
    QuestAlternativeCreateForm,
)
from core.models import (
    Jogador, Classe, Equipe, Quest, Classe
)
from core.choices import QuestLevel, JogadorClass, JogadorType

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
    template_name = "equipe/create.html"
    success_url = reverse_lazy('core:equipe_list')

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

    def dispatch(self, request, *args, **kwargs):
        jogador = request.user.jogador
        equipe = self.get_object()

        if (
            not Jogador.objects.is_lider(jogador, equipe=equipe) and
            not Jogador.objects.is_member(jogador, equipe=equipe)
        ):
            return HttpResponseForbidden()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        kwargs.update({
            'form':QuestAlternativeCreateForm,
        })

        return super(
            EquipeDetailView, self).get_context_data(**kwargs)


class EquipeDeleteView(LoginRequiredMixin, DeleteView):
    model = Equipe
    template_name = "equipe/delete.html"
    success_url = reverse_lazy('core:equipe_list')

    def dispatch(self, request, *args, **kwargs):
        jogador = request.user.jogador
        equipe = self.get_object()

        if jogador != equipe.lider or not equipe.open:
            return HttpResponseRedirect(reverse_lazy('core:404'))

        return super(
            EquipeDeleteView, self).dispatch(request, *args, **kwargs)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):
        equipe = self.get_object()

        logger.debug(
            f"equipe aqui: {equipe}"
        )

        related_quests = Quest.objects.filter(
            equipe=equipe
        )

        # related_quests.update(active=False)
        logger.debug(
            f"related_quests aqui: {related_quests}"
        )

        equipe.open = False
        # equipe.save()

        return HttpResponseRedirect(
            reverse(
                'core:equipe_delete',
                kwargs={'pk':equipe.pk}
            )
        )

        # return HttpResponseRedirect(self.get_success_url())



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

