import datetime
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

# class RenovarLivroForm(forms.Form):
#     data_de_renovação = forms.DateField(help_text="Insira uma data entre hoje e 4 semanas (padrão: 3).")

#     def clean_data_de_renovação(self):
#         """valida a data_de_renovação"""
#         data = self.cleaned_data['data_de_renovação'] # limpa a data de inputs potencialmente inseguros

#         # checa se a data não está no passado
#         if data < datetime.date.today():
#             raise ValidationError(_('Data inválida - renovação está no passado.'))

#         # checa se a data está dentro do lapso permitida
#         if data > datetime.date.today() + datetime.timedelta(weeks=4):
#             raise ValidationError(_('Data inválida - renovação superior a 4 semanas.')) # The example wraps this text in one of Django's translation functions ugettext_lazy() (imported as _()), which is good practice if you want to translate your site later.

#         # lembre-se de sempre retornar a data 'limpa'
#         return data

from django.forms import ModelForm
from catalog.models import LivroInstância

# forma simples de criar forms usando os fields de um Model apenas:
class RenovarLivroForm(ModelForm):

    def clean_data_de_renovação(self):
        """valida a data_de_renovação"""
        data = self.cleaned_data['data_de_devolução'] # limpa a data de inputs potencialmente inseguros

        # checa se a data não está no passado
        if data < datetime.date.today():
            raise ValidationError(_('Data inválida - renovação está no passado.'))

        # checa se a data está dentro do lapso permitida
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Data inválida - renovação superior a 4 semanas.')) # The example wraps this text in one of Django's translation functions ugettext_lazy() (imported as _()), which is good practice if you want to translate your site later.

        # lembre-se de sempre retornar a data 'limpa'
        return data

    class Meta:
        model = LivroInstância
        fields = ['data_de_devolução'] # como no exemplo de form para criar posts no djangogirls
        help_texts = {'data_de_devolução': _('Insira uma data entre hoje e 4 semanas (padrão 3).')} 