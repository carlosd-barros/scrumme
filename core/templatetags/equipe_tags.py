from django import template
from django.db.models import Q

from core.choices import JogadorType as JT
from core.choices import JogadorClass as JC
from core.models import Jogador, Quest, Equipe

register = template.Library()


@register.simple_tag
def get_related_quests(equipe):
    return Quest.objects.filter(
        equipe=equipe
    ).count()
