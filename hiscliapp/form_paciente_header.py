from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import Paciente

class Paciente_Header_Form(ModelForm):
    #Algunos datos del paciente para encabezado, no se pueden modificar
    class Meta:
        model = Paciente
        fields = '__all__'
    def __init__(self, selfpk, *args, **kwargs):
        html_inhabilitar_select =  """
		<script type="text/javascript">
		    $('#id_obra_social option:not(:selected)').attr('disabled',true);
		</script>
		"""		

        html_completar_texto = """
            <script type="text/javascript">
            $(function(){
                $('.link_completar').on('click', function() {
                    var textoPlantillaAntecedentesPersonales=   `
-HTA:
-Medicacion habitual:
-Dia:
-Sedentarismo:
-Obesidad:
-Tabaquismo:
-Actividad Fisica:
-QX:
-Dieta:
`;                
                    var prevSibling = $(this).siblings('.form-group').find('.textarea');
                    prevSibling.val(textoPlantillaAntecedentesPersonales);
                    setTimeout(
                      function() {
                        prevSibling.focus();
                      }, 100
                    );
                });
            });
            </script>
        """		
        super(Paciente_Header_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Paciente',
            Row(
                Div(Field('obra_social', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('numero_afiliado', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('apellido', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('nombres', readonly=True), css_class="col-xs-6 col-md-3")
            )
            ),
            FormActions(
                StrictButton('Volver sin guardar',
                    onclick="location.href='"+ reverse('hiscliapp:paciente_listar')+"'",
                        name="volver", value='volver a lista de pacientes', css_class="btn btn-default"),
            ),
            HTML(html_inhabilitar_select), 
            HTML(html_completar_texto),
        )

