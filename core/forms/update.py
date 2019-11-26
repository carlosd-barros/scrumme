import logging
from PIL import Image
from resizeimage import resizeimage

from django import forms
from django.conf import settings
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.core.exceptions import ValidationError
from django.template.defaultfilters import filesizeformat
from django.db.models import Q

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Div, Column, Row
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

from django.contrib.auth.models import User
from core.models import Jogador, Classe, Equipe, Quest

from .base import ModelBaseFormHelper, ModelDatePickerForm, BaseFormHelper

logger = logging.getLogger(__name__)


class JogadorUpdateForm(ModelBaseFormHelper):
    password1 = forms.CharField(
        label='Senha',
        widget= forms.PasswordInput,
        max_length=20,
        required=False
    )
    password2 = forms.CharField(
        label='Confirme sua senha',
        widget= forms.PasswordInput,
        max_length=20,
        required=False
    )
    avatar = forms.FileField(
        label='Avatar',
        required=False
    )

    class Meta:
        model = User
        fields = [
            'username', 'email',
            'first_name', 'last_name',
            # 'password1', 'password2',
            # 'avatar'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(JogadorUpdateForm, self).__init__(*args, **kwargs)
        self.helper.layout = Layout(
            'username',
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            'email',
            # Row(
            #     Column('password1', css_class='form-group col-md-6 mb-0'),
            #     Column('password2', css_class='form-group col-md-6 mb-0'),
            #     css_class='form-row'
            # ),
            # 'avatar',
        )

        if instance:
            self.fields['avatar'].initial = instance.jogador.avatar

    def clean_avatar(self):
        avatar = self.cleaned_data.get('avatar', None)

        if avatar:
            file_extension = avatar.name.split('.')[-1]

            try:
                print('verificando extensão do arquivo')
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
                    raise forms.ValidationError(_(
                        'Tipo de arquivo não suportado'
                    ))

            except:
                pass

        return avatar


# update quest normal
class QuestUpdateForm(ModelDatePickerForm):

    class Meta:
        model = Quest
        fields = [
            "name", "responsaveis",
            "init_date", "end_date",
            "points", "description"
        ]
        widgets = {
            'init_date': DatePicker(),
            'end_date': DatePicker(),
        }

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super(QuestUpdateForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['responsaveis'].queryset = instance.equipe.team.filter(active=True)
            self.fields['responsaveis'].required = True


# update quest para criar ou para que outros jogadores
# que não seja o lider da equipe possam atualizar os responsáveis
class QuestCompleteCreateForm(ModelBaseFormHelper):

    class Meta:
        model = Quest
        fields = ['responsaveis']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(QuestCompleteCreateForm, self).__init__(*args, **kwargs)

        if instance:
            team = instance.equipe.team.all()
            lider = Jogador.objects.filter(
                user=instance.equipe.lider.user
            )
            # self.fields['responsaveis'].queryset = instance.equipe.team.filter(active=True)
            self.fields['responsaveis'].queryset = team | lider
            self.fields['responsaveis'].required = True

