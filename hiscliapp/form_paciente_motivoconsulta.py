from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import Paciente, PacienteMotivoConsulta

class Paciente_MotivoConsulta_Form(ModelForm):
    fecha = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = PacienteMotivoConsulta
        fields = '__all__'

    def __init__(self, *args, **kwargs):
	
        super(Paciente_MotivoConsulta_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Motivo de consulta',
                Row(
                Div('fecha', css_class="col-xs-6 col-md-3"),
                Div('motivo_consulta', css_class="col-xs-6 col-md-8"),
                Div(
                    Field('Observaciones', style="height: 100px;"), 
                    css_class="h-50 col-xs-11 col-md-10"),
                Div('DELETE', css_class="input-small col-xs-1 col-md-2"), 
                ),            
            ),

            
        )
    def save(self, commit=True):
        instance = super(Paciente_MotivoConsulta_Form, self).save(commit= False)
        if commit:
            instance.save()
        return instance

motivo_consulta_InlineFormSet= inlineformset_factory(Paciente, 
               PacienteMotivoConsulta, fields ='__all__',
               form=Paciente_MotivoConsulta_Form, extra=1 )
