from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import VetDuenio

class VetDuenio_Header_Form(ModelForm):
    #Algunos datos del paciente para encabezado, no se pueden modificar
    class Meta:
        model = VetDuenio
        fields = '__all__'
    def __init__(self, selfpk, *args, **kwargs):
        super(VetDuenio_Header_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Propietario',
            Row(
                Div(Field('codigo', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('apellido', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('nombres', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('domicilio', readonly=True), css_class="col-xs-6 col-md-3"),
            )
            ),
            FormActions(
                StrictButton('Volver sin guardar',
                    onclick="location.href='"+ reverse('hiscliapp:vetduenio_listar')+"'",
                        name="volver", value='volver a lista de propietarios', css_class="btn btn-warning"),
            ),
        )

