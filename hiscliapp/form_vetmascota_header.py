from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions, StrictButton
from django.urls import reverse, reverse_lazy

from .models import VetMascota

class VetMascota_Header_Form(ModelForm):
    #Algunos datos del paciente para encabezado, no se pueden modificar
    class Meta:
        model = VetMascota
        fields = '__all__'
    def __init__(self, selfpk, *args, **kwargs):
        html_inhabilitar_select =  """
		<script type="text/javascript">
		    $('#id_especie option:not(:selected)').attr('disabled',true);
		    $('#id_sexo option:not(:selected)').attr('disabled',true);
		    $('#id_raza option:not(:selected)').attr('disabled',true);
		</script>
		"""				
        html_edad =  """
		<script type="text/javascript">
		    nacimiento= $('#id_fecha_nacimiento').val();
		    moment.locale('es');
            //texto_edad= moment(nacimiento, "DD/MM/YYYY").fromNow()
            let diferencia = moment(nacimiento, "DD/MM/YYYY").diff(moment(),'milliseconds')
            let duracion = moment.duration(diferencia)
            let texto_edad = "Nacimiento (" +(-1)* duracion.years() + " año/s " + (-1)*duracion.months() + " mes/es "+ (-1)*duracion.days() + " día/s )"
		    let label = $("label[for='"+$("#id_fecha_nacimiento").attr('id')+"']");
		    label.text(texto_edad);
		</script>
		"""					
        super(VetMascota_Header_Form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Fieldset('Mascota',
            Row(
                Div(Field('codigo', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('nombre', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('especie', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('raza', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('color', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('fecha_nacimiento', readonly=True), css_class="col-xs-6 col-md-3"),
                Div(Field('sexo', readonly=True), css_class="col-xs-6 col-md-3"),
            )
            ),
            FormActions(
                StrictButton('Volver sin guardar',
                    onclick="location.href='"+ reverse('hiscliapp:vetduenio_listar')+"'",
                        name="volver", value='volver a lista de due&ntilde;os', css_class="btn btn-warning"),
            ),
            HTML(html_inhabilitar_select),             
            HTML(html_edad),             
        )

