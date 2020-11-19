from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import Paciente, AntecedentesFamiliares
    
class AntecedentesFamiliares_Form(ModelForm):
    class Meta:
        model = AntecedentesFamiliares
        fields = '__all__'

    def __init__(self, *args, **kwargs):
	
        super(AntecedentesFamiliares_Form, self).__init__(*args, **kwargs)
        
      
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Antecedente familiar',
                Row(
                Div('tipo_cancer', css_class="col-xs-6 col-md-3"),
                Div('diabetes', css_class="col-xs-6 col-md-8"),
                Div('HTA', css_class="col-xs-6 col-md-8"),                
                Div('ACV', css_class="col-xs-6 col-md-8"),                
                Div(
                    Field('Observaciones', style="height: 100px;"), 
                    css_class="h-50 col-xs-11 col-md-10"),
                ),            
            ),      
        )
    def save(self, commit=True):
        instance = super(AntecedentesFamiliares_Form, self).save(commit= False)
        if commit:
            instance.save()
        return instance

antecedentes_familiares_InlineFormSet= inlineformset_factory(Paciente, 
               AntecedentesFamiliares, fields ='__all__',
               form=AntecedentesFamiliares_Form )

