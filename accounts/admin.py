from django.contrib import admin
from .models import Pessoa

@admin.register(Pessoa)
class PessoaAdmin(admin.ModelAdmin):
    list_display= ["name", "created", "updated", "active"]
    search_fields= ["user__first_name", "user__last_name"]
    readonly_fields = ["created","updated"]