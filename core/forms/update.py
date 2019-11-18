import logging
from PIL import Image
from resizeimage import resizeimage

from django import forms
from django.conf import settings
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Column, Row
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from django.contrib.auth.models import User
from core.models import Jogador, Classe, Equipe, Quest

from .base import ModelBaseFormHelper

logger = logging.getLogger(__name__)


class JogadorUpdateForm(ModelBaseFormHelper):
    avatar = forms.FileField(
        label='Avatar',
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            'avatar'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(JogadorUpdateForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['avatar'].initial = instance.jogador.avatar

    def clean_avatar(self):
        avatar = self.cleaned_data['avatar']

        if avatar:
            file_extension = avatar.name.split('.')[-1]

            logger.debug(
                f"{filesizeformat(settings.ALLOWED_UPLOAD_MAXSIZE)} | "
                f"{filesizeformat(avatar.size)}\n"
                f"{avatar.name}"
            )

            try:
                logger.debug('verificando extensão do arquivo')
                if file_extension in settings.ALLOWED_UPLOAD_FILETYPES:
                    logger.debug('verificando tamanho do arquivo')
                    if avatar.size > settings.ALLOWED_UPLOAD_MAXSIZE:

                        logger.debug('upload maximo permitido excedido')
                        raise forms.ValidationError(_(
                            f'Upload máximo permitido {filesizeformat(settings.ALLOWED_UPLOAD_MAXSIZE)}. '
                            'Atual {filesizeformat(avatar.size)}'
                        ))
                    else:
                        logger.debug('deu bom meu bacano')
                else:
                    logger.debug('tipo de arquivo não suportado')
                    raise forms.ValidationError(
                        _('Tipo de arquivo não suportado'))

            except AttributeError:
                pass

        return avatar
