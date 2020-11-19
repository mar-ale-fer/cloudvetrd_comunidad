from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy
from django.conf import settings

from .models import PacienteMotivoConsulta, ConsultaImagen
    
class ConsultaImagen_Form(ModelForm):
    imagen = forms.ImageField( required = False, widget=forms.FileInput)
    class Meta:
        model = ConsultaImagen
        fields = '__all__'

    def __init__(self, *args, **kwargs):
	
        super(ConsultaImagen_Form, self).__init__(*args, **kwargs)
        
      
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Imagen',
                Row(
                  Div(Field('imagen' , template='hiscliapp/util/ImageFieldTemplate.html'),
                   css_class="col-xs-6 col-md-3"),
                  Div('DELETE', css_class="input-small col-xs-1 col-md-2"), 
                ),            
            ),
        )
    def save(self, commit=True):
        instance = super(ConsultaImagen_Form, self).save(commit= False)
        if commit:
            instance.save()
        return instance

consulta_imagen_InlineFormSet= inlineformset_factory(PacienteMotivoConsulta, 
               ConsultaImagen, fields ='__all__',
               form=ConsultaImagen_Form, extra=1)
