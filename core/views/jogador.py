import logging
from PIL import Image
from resizeimage import resizeimage

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, render
from django.http.response import HttpResponse, HttpResponseRedirect

from django.db.models import Q
from django.db import transaction
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.defaultfilters import filesizeformat

from django.views.generic import (
    ListView, FormView, DetailView, 
    FormView,TemplateView, CreateView, 
    UpdateView, DeleteView, View
)

from core.models import Jogador, Classe, Equipe, Quest
from core.forms.update import JogadorUpdateForm

logger = logging.getLogger(__name__)


class JogadorListView(LoginRequiredMixin, ListView):
    model = Jogador
    template_name = "jogador/list.html"
    ordering = ["name"]


class JogadorDetailView(LoginRequiredMixin, DetailView):
    model = Jogador
    template_name = "jogador/detail.html"

    def dispatch(self, request, *args, **kwargs):
        jogador_user = self.get_object().user

        if not request.user == jogador_user:
            messages.error(
                request,
                'Usuário não possui permissão.'
            )

            return HttpResponseRedirect(
                reverse_lazy('core:home')
            )

        return super(
            JogadorDetailView, self).dispatch(request, *args, **kwargs)


class JogadorDeleteView(LoginRequiredMixin, DeleteView):
    model = Jogador
    success_url = reverse_lazy('accounts:login')
    template_name = "jogador/delete.html"


class JogadorUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = JogadorUpdateForm
    template_name = 'jogador/update.html'
    success_url = 'core:jogador_detail'

    @transaction.atomic
    def form_valid(self, form):
        if self.request.method == 'POST':

            if form.is_valid():
                data = form.cleaned_data
                avatar = data.get('avatar', None)
                new_name = f"{data.get('first_name')} {data.get('last_name')}"
                user = self.request.user
                jogador = user.jogador

                jogador.name = new_name

                if avatar:
                    logger.debug(f"avatar aqui: {avatar}")
                    resized_avatar = self.format_image(jogador.avatar)

                    if resized_avatar:
                        jogador.avatar = avatar
                        jogador.save()

                        logger.debug(f"resized_avatar aqui: {resized_avatar}")
                        jogador.avatar = resized_avatar

                jogador.save()
                form.save()

                messages.success(
                    self.request, "Perfil atualizado com sucesso."
                )

        return super(
            JogadorUpdateView, self).form_valid(form)

    def format_image(self, img):
        try:
            logger.debug('iniciando processo de redimensionamento de imagem')
            with open(img.path, 'r+b') as file:
                logger.debug('alterando dimenções do arquivo')
                with Image.open(file) as image:
                    logger.debug(f"imagem antes: {img.size} | {img.size}")
                    cover = resizeimage.resize_cover(image, [150, 150])
                    cover.save(img.path, image.format)
                    logger.debug('fim do processo de redimensionamento')

            logger.debug(f"imagem depois: {image.size} | {img.size}")
            return img

        except AttributeError as error:
            logger.debug(f'deu ruim meu bacano: {error}')
            messages.error(
                self.request,
                f"error ao alterar avatar."
            )
            return None


    def get_success_url(self):
        return reverse(
            self.success_url,
            kwargs=({
                'pk':self.get_object().jogador.pk
            })
        )
