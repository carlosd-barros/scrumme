from django import template
from django.db.models import Q

from core.choices import JogadorType as JT
from core.choices import JogadorClass as JC
from core.models import Jogador, Quest, Equipe

register = template.Library()


# @register.simple_tag(takes_context=True)
@register.simple_tag
def get_equipes(jogador):
    return Equipe.objects.filter(
        (
            Q(lider=jogador) | Q(team__in=[jogador])
        ) &
        Q(active=True)
    ).distinct()


@register.simple_tag
def get_quests(jogador):
    return Quest.objects.filter(
        Q(responsaveis__in=[jogador]) |
        Q(equipe__in = get_equipes(jogador=jogador) )
    ).distinct()


@register.simple_tag
def get_jogador_type(type):
    return [
        t.display_name for t in JT if t.code == type
    ][0].capitalize()


@register.simple_tag
def get_jogador_class(classe):
    return [
        c.display_name for c in JC if c.code == classe
    ][0].capitalize()


@register.simple_tag
def is_master_or_lider(jogador, quest=None, equipe=None):
    if quest:
        if jogador == quest.equipe.lider:
            return True

    if equipe:
        if jogador == equipe.lider:
            return True

    return False
