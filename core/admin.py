from django.contrib import admin
from .models import Equipe

@admin.register(Equipe)
class EquipeAdmin(admin.ModelAdmin):
    list_display= ['name', 'created', 'updated', 'active']
    readonly_fields = ['created','updated']
    filter_horizontal = ['dev_team']
    search_fields = [
        'name',
        'product_owner__name',
        'scrum_master__name'
    ]