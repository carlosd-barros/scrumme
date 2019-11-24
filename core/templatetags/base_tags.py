from django import template
from django.db.models import Q

from core.choices import JogadorType as JT
from core.choices import JogadorClass as JC
from core.models import Jogador, Quest, Equipe

register = template.Library()


@register.simple_tag
def is_lider(jogador, equipe=None, quest=None):
    if jogador.user.is_superuser:
        return True

    elif equipe:
        return Jogador.objects.is_lider(
            jogador, equipe=equipe
        )

    elif quest:
        return Jogador.objects.is_lider(
            jogador, quest=quest
        )

    return False


@register.simple_tag(takes_context=True)
def is_member(context, equipe=None, quest=None):
    jogador = context.get('request').user.jogador

    if jogador.user.is_superuser:
        return True

    elif equipe:
        return Jogador.objects.is_member(
            jogador, equipe=equipe
        )

    elif quest:
        return Jogador.objects.is_member(
            jogador, quest=quest
        )

    return False
