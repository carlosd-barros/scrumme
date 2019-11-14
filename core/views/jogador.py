import logging

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.views.generic import (
    ListView, FormView, DetailView, 
    FormView,TemplateView, CreateView, 
    UpdateView, DeleteView, View
)

from core.models import Jogador, Classe, Equipe, Quest

logger = logging.getLogger(__name__)


class JogadorListView(LoginRequiredMixin, ListView):
    model = Jogador
    template_name = "jogador/list.html"
    ordering = ["name"]
    paginate_by = 5

@transaction.atomic
class JogadorCreateView(CreateView):
    model = Jogador
    template_name = "jogador/create.html"
    fields = [
        "name", "jogador",
        "init_date", "end_date",
        "points", "description"
    ]


class JogadorDetailView(LoginRequiredMixin, DetailView):
    model = Jogador
    template_name = "jogador/detail.html"

class JogadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Jogador
    success_url = reverse_lazy('accounts:login')
    template_name = "jogador/delete.html"


class JogadorUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'jogador/update.html'
    success_url = 'core:jogador_detail'
    fields = [
        'username', 'email',
        'first_name', 'last_name'
    ]

    @transaction.atomic
    def form_valid(self, form):
        if self.request.method == 'POST':

            if form.is_valid():
                data = form.cleaned_data
                user = form.save()

                j = Jogador.objects.get(
                    user = self.request.user
                )
                j.name = (
                    f"{data.get('first_name')} "
                    f"{data.get('last_name')}"
                )
                j.save()

                messages.success(
                    self.request,
                    "Perfil atualizado com sucesso."
                )
        else:
            messages.error(
                self.request,
                'Ops, parece que algo deu errado.'
            )
            form = self.get_form()
            render(
                self.request, self.template_name, {'form':form}
            )

        return super(
            JogadorUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse(
            self.success_url,
            kwargs=({
                'pk':self.get_object().jogador.pk
            })
        )
