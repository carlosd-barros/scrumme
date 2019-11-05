from django import forms
from core.models import Jogador, Classe, Equipe, Quest


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
        help_text='Mantenha precionado ctrl para celecionar vários'
    )

    class Meta:
        model = Equipe
        fields = [
            "name", "lider", "team"
        ]

