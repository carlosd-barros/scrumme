from django import template
from django.db.models import Q

from core.choices import JogadorType as JT
from core.models import Jogador, Quest, Equipe

register = template.Library()


@register.simple_tag(takes_context=True)
def get_equipes(context, jogador):
    return Equipe.objects.filter(
        Q(lider=jogador) |
        Q(team__in=[jogador])
    ).distinct()


@register.simple_tag
def get_quests(jogador):
    return Quest.objects.filter(
        responsaveis__in=[jogador]
    ).distinct()


@register.simple_tag
def get_jogador_type(type):
    return [
        t.display_name for t in JT if t.code == type
    ][0]
