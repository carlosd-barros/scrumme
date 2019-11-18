from django import forms
from django.core.exceptions import ValidationError

from crispy_forms.helper import FormHelper
from core.models import Jogador, Classe, Equipe, Quest
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker


class ModelBaseFormHelper(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper(self)
        self.helper.form_tag = False
        self.helper.include_media = False


class ModelDatePickerForm(ModelBaseFormHelper):

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
            'node_modules/moment/min/moment.min.js',
        )

