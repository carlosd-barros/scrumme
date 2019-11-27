from django import template
from django.db.models import Q

from core.models import Jogador, Quest, Equipe

register = template.Library()


@register.simple_tag
def is_lider(jogador, equipe=None, quest=None):
    # if jogador.user.is_superuser:
    #     return True

    if equipe:
        return Jogador.objects.is_lider(
            jogador, equipe=equipe
        )

    elif quest:
        return Jogador.objects.is_lider(
            jogador, quest=quest
        )

    return False


# @register.simple_tag(takes_context=True)
@register.simple_tag
def is_member(jogador, equipe=None, quest=None):

    # if jogador.user.is_superuser:
    #     return True

    if equipe:
        return Jogador.objects.is_member(
            jogador, equipe=equipe
        )

    elif quest:
        return Jogador.objects.is_member(
            jogador, quest=quest
        )

    return False

@register.simple_tag
def is_lider_or_member(jogador, equipe=None, quest=None):

    is_lider = Jogador.objects.is_lider(
        jogador=jogador, equipe=equipe, quest=quest
    )

    is_member = Jogador.objects.is_member(
        jogador=jogador, equipe=equipe, quest=quest
    )

    return is_lider or is_member
