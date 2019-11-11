from django.contrib import admin
from .models import Equipe, Quest, Classe, Jogador

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display= ['name', 'created', 'updated', 'active']
    readonly_fields = ['created','updated']
    filter_horizontal = ['team']
    search_fields = ['name']
    prepopulated_fields = {
        "slug": ("name",)
    }

@admin.register(Quest)
class QuestAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'init_date',
        'end_date', 'points',
    ]
    readonly_fields = ['created']
    filter_horizontal = ['responsaveis']
    search_fields = [
        'name',
        'jogador__user__username',
        'jojador__name'
    ]
    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",)
    }


@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        "slug": ("name",)
    }
