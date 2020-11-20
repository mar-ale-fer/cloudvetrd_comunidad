from django.forms import ModelForm, BaseInlineFormSet, BaseFormSet
from django import forms
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy
from crum import get_current_user

from .models import VetMascota, VetConsulta
from .models import VetPersonal

"""
baseinlineformset:
https://reinbach.com/blog/django-formsets-with-extra-params/
https://stackoverflow.com/questions/21875555/inline-formset-factory-pass-request-to-child-form
"""  
class BaseFormSet(BaseInlineFormSet):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super(BaseFormSet, self).__init__(*args, **kwargs)               	
    def _construct_form(self, i, **kwargs):
        if 'clinica' not in self.request.session:
            id_clinica = 0
        else:
            id_clinica = int(self.request.session['clinica'])		
        form = super(BaseFormSet, self)._construct_form(i, **kwargs)
        form.fields["atendio"].queryset = VetPersonal.objects.filter(clinica__id = id_clinica)        	
        return form
class VetMascota_VetConsulta_Form(ModelForm):
    fecha = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
    observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
       
    class Meta:
        model = VetConsulta
        fields = '__all__'

    def __init__(self, *args, **kwargs):

        super(VetMascota_VetConsulta_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Consulta',
                Row(
                  Div('fecha', css_class="col-xs-6 col-md-2"),
                  Div('motivo_consulta', css_class="col-xs-6 col-md-2"),
                  Div('peso', css_class="col-xs-3 col-md-2"),
                  Div(
                    Field('observaciones'), 
                    css_class="col-xs-9 col-md-6"),
                  Div('atendio', css_class="col-xs-3 col-md-2"),
                  Div('cuenta_corriente', css_class="col-xs-3 col-md-2"),
                  Div('DELETE', css_class="input-small col-xs-2 col-md-2"),
                ),            
            ),
        )
    def save(self, commit=True):
        instance = super(VetMascota_VetConsulta_Form, self).save(commit= False)
        if commit:
            instance.save()
        return instance

 
        
vetconsulta_InlineFormSet= inlineformset_factory(VetMascota, 
               VetConsulta, fields ='__all__',
               formset=BaseFormSet,
               form=VetMascota_VetConsulta_Form, extra=1 )
