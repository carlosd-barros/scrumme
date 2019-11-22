import logging
from random import randint

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
    UpdateView, DeleteView, View,
)

from core.forms.create import QuestCreateForm, QuestAlternativeCreateForm
from core.forms.update import (
    QuestUpdateForm, QuestCompleteCreateForm,
)
from core.models import (
    Jogador, Classe, Equipe, Quest, Classe
)
from core.choices import QuestLevel, JogadorClass, JogadorType

logger = logging.getLogger(__name__)


class QuestListView(LoginRequiredMixin, ListView):
    model = Quest
    template_name = "quest/list.html"
    ordering = ["-created"]

    def get_queryset(self):
        jogador = self.request.user.jogador
        equipe = Equipe.objects.filter(
            Q(lider=jogador) | Q(team__in=[jogador])
        ).distinct()

        return super().get_queryset().filter(
            Q(responsaveis__in=[jogador]) | Q(equipe__in=equipe)
        ).distinct()


class QuestDetailView(LoginRequiredMixin, DetailView):
    model = Quest
    template_name = "quest/detail.html"

    # def dispatch(self, request, *args, **kwargs):
    #     user = request.user
    #     jogador = user.jogador


    #     return super(
    #         QuestDetailView, self).dispatch(request, *args, **kwargs)


class QuestUpdateView(LoginRequiredMixin, UpdateView):
    model = Quest
    form_class = QuestUpdateForm
    template_name = "quest/update.html"
    success_url = 'core:quest_detail'

    @transaction.atomic
    def form_valid(self, form):
        if self.request.method == 'POST':
            if form.is_valid:
                form.save()

                messages.success(
                    self.request, 'Quest editada com sucesso.'
                )
                return HttpResponseRedirect(self.get_success_url())

            messages.error(
                self.request, 'Ops, verifique os dados informados.'
            )
            return render(
                self.request, self.template_name, context={'form':form}
            )

        return reverse_lazy('core:quest_list')

    def get_success_url(self):
        return reverse(
            self.success_url, kwargs={'pk':self.get_object().pk}
        )


# Criar quest a partir de uma equipe
class QuestAlternativeCreateView(LoginRequiredMixin, CreateView):
    model = Quest
    form_class = QuestAlternativeCreateForm
    success_url = 'core:quest_detail'

    def dispatch(self, request, *args, **kwargs):
        logger.debug('opa passou aqui hein')
        return super().dispatch(request, *args, **kwargs)

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        form = QuestAlternativeCreateForm(request.POST)

        if form.is_valid:
            quest = form.save(commit=False)
            points = self.points_for_quest(quest.level)

            if points:
                quest.points = points

            else:
                messages.error(
                    request,
                    'Os pontos desta quest não puderam ser atribuídos.'
                )

            quest.equipe = get_object_or_404(
                Equipe, pk=kwargs.get('pk', None)
            )
            quest.save()

            messages.success(
                self.request,
                'Quest criada com sucesso. Agora defina os responsáveis.'
            )

            return HttpResponseRedirect(
                reverse(
                    'core:quest_alternative_update', kwargs={'pk':quest.pk}
                )
            )

        messages.error(
            self.request, 'Ops, verifique os dados do formulário.'
        )

        return HttpResponseRedirect(
            reverse('core:equipe_detail', kwargs={'pk':kwargs.get('pk')})
        )

    def points_for_quest(self, level):
        points = None

        if level == QuestLevel.BAIXO.code:
            points = randint(3,5)

        elif level == QuestLevel.MEDIO.code:
            points = randint(4,9)

        elif level == QuestLevel.ALTO.code:
            points = randint(10,15)

        return points


class QuestConcludeView(LoginRequiredMixin, View):
    success_url = reverse_lazy('core:quest_list')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        quest_pk = kwargs.get('pk', None)
        quest = get_object_or_404(Quest, pk=quest_pk)
        jogadores = quest.responsaveis.all()

        if jogadores.exists():
            for jogador in jogadores:
                classe = self.player_level_up(jogador, quest)
                if classe:
                    jogador.classe = classe

                jogador.points += quest.points
                jogador.save()

            quest.open = False
            quest.save()

            return HttpResponseRedirect(self.success_url)

        messages.error(
            request,
            'Por favor, defina um ou mais responsáveis por está quests.'
        )

        return HttpResponseRedirect(
            reverse(
                'core:quest_detail', kwargs={'pk':quest_pk}
            )
        )

    def player_level_up(self, jogador=None, quest=None):
        classe = None

        if jogador and quest:
            classe = jogador.classe
            points = jogador.points + quest.points

            current_class = Classe.objects.get(
                active=True,
                related_choice__exact=classe
            )
            next_class = Classe.objects.get(
                active=True,
                min_points__lte=points,
                max_points__gte=points
            )
            check_next_class = Classe.objects.get(
                active=True,
                min_points__exact=current_class.max_points+1
            )
            logger.debug(
                f"classe: {classe} | points: {points}\n"
            )
            logger.debug(
                f"current_class: {current_class} | next_class: {next_class}\n"
            )

            # next_class = next_class.first()

            if current_class == next_class:
                if self.request.user.jogador == jogador:
                    messages.success(
                        self.request,
                        f"{jogador.user.first_name}, faltam "
                        f"{next_class.min_points - points} "
                        f"para você ascender à classe {next_class.name}."
                    )

            elif next_class == check_next_class:
                if self.request.user.jogador == jogador:
                    classe = next_class.related_choice
                    messages.success(
                        self.request,
                        f"Parabéns {jogador.user.first_name}, "
                        f"você acaba de ascender à classe {next_class.name}"
                    )

            else:
                messages.error(
                    self.request,
                    f"Se você possui mais de {current_class.max_points+1} pontos "
                    f"e ainda está na classe {current_class.name}, por favor "
                    "mande um email para scrum.gamification@gmail.com "
                    "ou contate os administradores para que possamos corrigir isto."
                )

        return classe


class QuestDoneUpdateView(LoginRequiredMixin, UpdateView):
    model = Quest
    template_name = "quest/update.html"
    form_class = QuestCompleteCreateForm
    success_url = 'core:quest_detail'

    @transaction.atomic
    def form_valid(self, form):
        if self.request.method == 'POST':
            quest = self.get_object()
            logger.debug(f"nível aqui: {quest.level}")

            if form.is_valid:
                form.save()

                return HttpResponseRedirect(self.get_success_url())

        return render(
            self.request,
            self.template_name,
            context={'form':form, 'object':quest}
        )

    def get_success_url(self):
        return reverse(
            self.success_url, kwargs={'pk':self.get_object().pk}
        )


class QuestDeleteView(LoginRequiredMixin, DeleteView):
    model = Quest
    template_name = "quest/delete.html"
    success_url = reverse_lazy('core:quest_list')

