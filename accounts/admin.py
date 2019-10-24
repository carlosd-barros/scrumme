from django.contrib import admin
from .models import Jogador

@admin.register(Jogador)
class JogadorAdmin(admin.ModelAdmin):
    list_display= ["name", "created", "updated", "active"]
    search_fields= ["user__first_name", "user__last_name"]
    readonly_fields = ["created","updated"]