from django import forms
from core.models import Jogador, Classe, Equipe, Quest
from datetime import date

class EquipeCreateForm(forms.ModelForm):
    name = forms.CharField(
        label='Nome',
        max_length=150
    )
    lider = forms.ModelChoiceField(
        label='Lider da equipe',
        queryset=Jogador.objects.filter(active=True)
    )
    team = forms.ModelMultipleChoiceField(
        label='Integrantes do time',
        queryset=Jogador.objects.filter(active=True),
        help_text='Mantenha precionado ctrl para selecionar vários'
    )

    class Meta:
        model = Equipe
        fields = [
            "name", "lider", "team"
        ]


class QuestCreateForm(forms.ModelForm):
    init_date = forms.DateField(
        label='Data inicial',
        widget=forms.widgets.DateInput(
            attrs={
                'class':'datepicker',
                'style':"display:flex;",
            }
        ),
        required = True
    )
    end_date = forms.DateField(
        label='Data de entrega',
        widget=forms.widgets.DateInput(
            attrs={
                'class':'datepicker'
            }
        ),
        required = False
    )

    class Meta:
        model = Quest
        fields = [
            "name", "responsaveis",
            "init_date", "end_date",
            "points", "description"
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        super(QuestCreateForm, self).__init__(*args, **kwargs)

        if instance:
            self.fields['init_date'].widget.attrs['value'] = instance.init_date

            if instance.end_date:
                self.fields['end_date'].widget.attrs['value'] = instance.end_date

