from django import forms
from core.models import Jogador, Classe, Equipe, Quest


class EquipeCreateForm(forms.ModelForm):
    
    class Meta:
        model = Equipe
        fields = (
            "name", "lider", "team"
        )
