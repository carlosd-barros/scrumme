import logging
from random import randint

from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
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

    def dispatch(self, request, *args, **kwargs):
        jogador = request.user.jogador
        quest = self.get_object()

        if (
            not Jogador.objects.is_lider(jogador, quest=quest) and
            not Jogador.objects.is_member(jogador, quest=quest)
        ):
            return HttpResponseForbidden()

        return super(
            QuestDetailView, self).dispatch(request, *args, **kwargs)


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
class QuestAlternativeCreateView(LoginRequiredMixin, View):
    model = Quest
    form_class = QuestAlternativeCreateForm
    success_url = reverse_lazy('core:quest_list')

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        equipe = get_object_or_404(
            Equipe, pk=kwargs.get('pk', None)
        )
        form = self.form_class(request.POST)

        if form.is_valid():
            quest = form.save(commit=False)
            points = self.points_for_quest(quest.level)

            if points:
                quest.points = points

            else:
                messages.error(
                    request,
                    'Os pontos desta quest não puderam ser atribuídos.'
                )

            quest.equipe = equipe
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

        return render(
            self.request,
            "equipe/detail.html",
            {'form':form, 'object':equipe}
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

    def dispatch(self, request, *args, **kwargs):
        quest_id = kwargs.get('pk', None)
        quest = get_object_or_404(Quest, pk=quest_id)

        url_redirect = reverse(
            'core:quest_detail', kwargs={'pk':quest_id}
        )

        if not quest.open:
            messages.error(
                request, 'Esta quest já foi concluída.'
            )
            return HttpResponseRedirect(url_redirect)

        return super().dispatch(request, *args, **kwargs)

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
            'Por favor, defina um ou mais responsáveis por esta quests.'
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

            logger.debug(
                f"current_class: {current_class} | next_class: {next_class}\n"
            )

            if current_class == next_class:
                print("player_level_up primeiro condicional ")
                next_class = Classe.objects.get(
                    min_points__exact=current_class.max_points+1
                )
                if self.request.user.jogador == jogador:
                    messages.success(
                        self.request,
                        f"{jogador.user.first_name}, faltam "
                        f"{next_class.min_points - points} "
                        f"para você ascender à classe {next_class.name}."
                    )

            elif next_class:
                print("player_level_up segundo condicional ")
                if self.request.user.jogador == jogador:
                    classe = next_class.related_choice
                    messages.success(
                        self.request,
                        f"Parabéns {jogador.user.first_name}, "
                        f"você acaba de ascender à classe {next_class.name}."
                    )

            else:
                messages.error(
                    self.request,
                    f"Se você possui mais de {current_class.max_points+1} pontos "
                    f"e ainda esta na classe {current_class.name}, por favor "
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

