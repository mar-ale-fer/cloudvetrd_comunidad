from django.forms import ModelForm
from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import VetDuenio, VetMascota

class VetDuenio_VetMascota_Form(ModelForm):
    fecha_nacimiento = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    class Meta:
        model = VetMascota
        fields = '__all__'

    def __init__(self, *args, **kwargs):
	
        super(VetDuenio_VetMascota_Form, self).__init__(*args, **kwargs)
        self.fields['codigo'].disabled= True
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Mascota',
                Row(
                  Div('codigo', css_class="col-xs-6 col-md-2"),
                  Div('nombre', css_class="col-xs-6 col-md-2"),
                  Div('fecha_nacimiento', css_class="col-xs-6 col-md-2"),
                  Div('especie', css_class="col-xs-6 col-md-2"),
                  Div('raza', css_class="col-xs-6 col-md-2"),      
                  Div('color', css_class="col-xs-6 col-md-2"),
                  Div('sexo', css_class="col-xs-6 col-md-2"),
                  Div('DELETE', css_class="input-small col-xs-1 col-md-2"), 
                ),            
            ),

            
        )
    def save(self, commit=True):
        instance = super(VetDuenio_VetMascota_Form, self).save(commit= False)
        if commit:
            instance.save()
        return instance

vetmascota_InlineFormSet= inlineformset_factory(VetDuenio, 
               VetMascota, fields ='__all__',
               form=VetDuenio_VetMascota_Form, extra=1 )
