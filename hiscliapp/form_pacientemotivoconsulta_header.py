from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import PacienteMotivoConsulta

class PacienteMotivoConsulta_Header_Form(ModelForm):
    #Algunos datos del paciente para encabezado, no se pueden modificar
    class Meta:
        model = PacienteMotivoConsulta
        fields = '__all__'
    def __init__(self, selfpk, *args, **kwargs):
        html_inhabilitar_select =  """
		<script type="text/javascript">
		    $('#id_paciente option:not(:selected)').attr('disabled',true);
		</script>
		"""		

        super(PacienteMotivoConsulta_Header_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Consulta',
            Row(
                Div(Field('paciente', readonly=True), css_class="col-xs-6 col-md-3"), #parahacer:cambiar combo por texto para optimizar cuando tenga muchos pacientes
                Div(Field('fecha', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('motivo_consulta', readonly=True), css_class="col-xs-6 col-md-3"),
            )
            ),
            FormActions(
                StrictButton('Volver sin guardar',
                    onclick="location.href='"+ reverse('hiscliapp:paciente_listar')+"'",
                        name="volver", value='volver a lista de pacientes', css_class="btn btn-default"),
            ),
            HTML(html_inhabilitar_select), 
        )

