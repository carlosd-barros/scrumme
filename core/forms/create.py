import logging
from datetime import date

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _

from crispy_forms.helper import FormHelper
from tempus_dominus.widgets import (
    DatePicker, TimePicker, DateTimePicker
)

from core.models import (
    Jogador, Classe, Equipe, Quest
)
from .base import ModelDatePickerForm

logger = logging.getLogger(__name__)


class EquipeCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome',
        max_length=150
    )
    lider = forms.ModelChoiceField(
        required=True,
        label='Lider da equipe',
        queryset=Jogador.objects.filter(active=True),
    )
    team = forms.ModelMultipleChoiceField(
        required=True,
        label='Integrantes do time',
        queryset=Jogador.objects.filter(active=True),
        help_text='Mantenha precionado ctrl para selecionar vários'
    )

    class Meta:
        model = Equipe
        fields = [
            "name", "lider", "team"
        ]

class QuestCreateForm(ModelDatePickerForm):

    class Meta:
        model = Quest
        fields = [
            "name", "init_date",
            "end_date", "level",
            "description"
        ]
        widgets = {
            'init_date': DatePicker(),
            'end_date': DatePicker(),
        }


class QuestAlternativeCreateForm(ModelDatePickerForm):
    class Meta:
        model = Quest
        fields = [
            "name", "init_date",
            "end_date", "level",
            "description"
        ]
        widgets = {
            'init_date': DatePicker(),
            'end_date': DatePicker(),
        }

    def clean(self):
        cleaned_data = super(QuestAlternativeCreateForm, self).clean()
        init_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")
        today = date.today()

        if end_date and end_date < start_date:
            raise ValidationError(
                _("A data final não pode ser menor que a data inicial."))

        if start_date.date() < today:
            raise ValidationError(
                _("A data inicial não pode ser menor que a data de hoje."))


