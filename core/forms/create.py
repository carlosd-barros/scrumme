from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from tempus_dominus.widgets import (
    DatePicker, TimePicker, DateTimePicker
)

from core.models import (
    Jogador, Classe, Equipe, Quest
)
from .base import ModelDatePickerForm


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
            "name", "equipe", "responsaveis",
            "init_date", "end_date",
            "points", "description"
        ]
        widgets = {
            'init_date': DatePicker(),
            'end_date': DatePicker(),
        }

class QuestFormCreate(ModelDatePickerForm):

    class Meta:
        model = Quest
        fields = [
            "name", "init_date",
            "end_date", "points",
            "description"
        ]
        widgets = {
            'init_date': DatePicker(),
            'end_date': DatePicker(),
        }
