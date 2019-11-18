from django import forms
from datetime import date
from crispy_forms.helper import FormHelper
from core.models import Jogador, Classe, Equipe, Quest
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class ModelDatePickerForm(forms.ModelForm):

    class Media:
        css = {
            'all': (
                # 'node_modules/jquery-datetimepicker/build/'
                # 'jquery.datetimepicker.min.css',
                # 'node_modules/@fortawesome/fontawesome-free/css/all.min.css',
            )
        }
        js = (
            'node_modules/jquery/dist/jquery.slim.js',
            'node_modules/popper.js/dist/popper.min.js',
        )


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


class QuestCreateForm(ModelDatePickerForm):

    def __init__(self, *args, **kwargs):
        super(QuestCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.include_media = False


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


    # def __init__(self, *args, **kwargs):
    #     instance = kwargs.get('instance')
    #     super(QuestCreateForm, self).__init__(*args, **kwargs)

    #     if instance:
    #         self.fields['init_date'].widget.attrs['value'] = instance.init_date

    #         if instance.end_date:
    #             self.fields['end_date'].widget.attrs['value'] = instance.end_date


# def clean_document(self):
#     document = self.cleaned_data['document']

#     if document:
#         try:
#             if document.content_type in settings.ALLOWED_UPLOAD_FILETYPES:
#                 if document.size > settings.ALLOWED_UPLOAD_MAXSIZE:
#                     raise forms.ValidationError(
#                         _('Upload máximo permitido %s. Atual %s') % (
#                             filesizeformat(
#                                 settings.ALLOWED_UPLOAD_MAXSIZE),
#                             filesizeformat(document.size)))
#             else:
#                 raise forms.ValidationError(
#                     _('O arquivo informado não é um PDF.'))
#         except AttributeError:
#             pass

#     return document
