from django import template
from django.db.models import Q

from core.choices import JogadorType as JT
from core.choices import JogadorClass as JC
from core.models import Jogador, Quest, Equipe

register = template.Library()


@register.simple_tag(takes_context=True)
def is_lider(context, equipe):
    lider = equipe.equipe.lider
    jogador = context.get('request').user.jogador
    
    if lider == jogador:
        return True

    return False

@register.simple_tag(takes_context=True)
def member_permission(context, quest):
    jogador = context.get('request').user.jogador

    if jogador in quest.responsaveis.all():
        return True

    return False

