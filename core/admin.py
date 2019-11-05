from django.contrib import admin
from .models import Equipe, Quest, Classe, Jogador

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display= ['name', 'created', 'updated', 'active']
    readonly_fields = ['created','updated']
    filter_horizontal = ['team']
    search_fields = ['name']

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'init_date',
        'end_date', 'points',
    ]
    readonly_fields = ['created']
    search_fields = [
        'name',
        'jogador__user__username',
        'jojador__name'
    ]


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    pass


@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    pass
