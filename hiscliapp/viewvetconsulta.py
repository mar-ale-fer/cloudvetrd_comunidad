 # -- coding: utf-8 --
from django import forms
from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import HTML,Div,Field,Layout, Fieldset, ButtonHolder, Submit, Row
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions,StrictButton
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.db.models import Q #para OR en consultas
from django.db.models.deletion import ProtectedError
from django.forms import ValidationError

from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PropietarioMixin
from django.shortcuts import get_object_or_404

vetconsulta_fields = (
'mascota',
'fecha',
'motivo_consulta',
'peso',
'observaciones',
'cuenta_corriente',
'atendio'
)

from .models import VetConsulta
from .models import VetMascota
from .models import VetPersonal

class DateInput(forms.DateInput):
  input_type = 'date'

class VetConsultataDetalle(LoginRequiredMixin,PropietarioMixin, DetailView):
    model = VetConsulta
    fields = vetconsulta_fields

"""
Crear y modificar
"""
class VetConsultaForm(ModelForm):
  fecha = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
  observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))

  def __init__(self, selfpk, vetmascota_id, id_clinica, modo, *args, **kwargs):

    html_focus_fecha = """
        <script type="text/javascript">    
        window.onload = function() {
        document.getElementById("id_fecha").focus();
        };
        </script>
        """ 

    if modo == 'INS': 
      html_inhabilitar_eliminar = """
        <script type="text/javascript">
        //espero medio segundo e inhabilito
        setTimeout(
        function() {
            $('#btn_eliminar').prop('disabled', true);
        }, 500);
        </script>
      """
    else:
      html_inhabilitar_eliminar = ""

    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
        Fieldset('Consulta',
        Row(
        Div('fecha', css_class="col-xs-12 col-md-6"),                
        Div('motivo_consulta', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('mascota', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('peso', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('observaciones', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('cuenta_corriente', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('atendio', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        HTML(html_focus_fecha),
        )),
        FormActions(
          Submit('save', 'Guardar', css_class='btn-success'),
          StrictButton('Volver a la mascota',
          onclick="location.href='"+reverse('hiscliapp:vetmascota_detalle', kwargs={'pk': vetmascota_id})+"'", #vuelve a la mascota
          name="volver",value='volver a la mascota' , css_class="btn btn-warning"),

          StrictButton('Eliminar',
          onclick="location.href='"+"/hiscliapp/vetconsulta/"+ str(selfpk) +"/borrar/"+ "'",
          id="btn_eliminar",
          name="eliminar",value='eliminar consulta' , css_class="btn btn-danger"),  


        ),
        HTML(html_inhabilitar_eliminar),
    )

    super(VetConsultaForm, self).__init__(*args, **kwargs)

    self.fields['mascota'].queryset= VetMascota.objects.filter(id=vetmascota_id)
    print('------')
    print(id_clinica)
    filtro_id_clinica = int(id_clinica)
    self.fields['atendio'].queryset= VetPersonal.objects.filter(clinica__id = int(filtro_id_clinica))

    #self.fields['mascota'].disabled= True
  class Meta:
    model = VetConsulta
    fields = vetconsulta_fields

class VetConsultaCrear(LoginRequiredMixin, CreateView):
    model = VetConsulta
    form_class = VetConsultaForm 
    #fields = paciente_fields

    def get_success_url(self):
        return reverse('hiscliapp:vetmascota_detalle', kwargs={'pk': self.object.mascota.pk,}) #vuelve a la mascota
    def get_form_kwargs(self):
      kwargs = super(VetConsultaCrear, self).get_form_kwargs()

      vetmascota_id = self.kwargs['vetmascota_id']
      unamascota =VetMascota.objects.get( id = vetmascota_id)
      id_clinica = int(unamascota.id_clinica())

      kwargs.update({
        'selfpk':0,
        'modo': 'INS',
        'vetmascota_id':vetmascota_id,
        'id_clinica':id_clinica,

        }) #pk= 0 todavia no existe
      return kwargs

    def get_initial(self):
        initial = super().get_initial()
        # cpf - it's the name of the field on your current form
        # self.args will be filled from URL. I'd suggest to use named parameters
        # so you can access e.g. self.kwargs['cpf_initial']
        vetmascota_id = self.kwargs['vetmascota_id']

        #al crear, la mascota viene por parámetros
        unamascota= get_object_or_404(VetMascota, pk=vetmascota_id)
        initial['mascota'] = unamascota

        return initial

class VetConsultaModificar(LoginRequiredMixin,PropietarioMixin, UpdateView):
    model = VetConsulta
    form_class = VetConsultaForm

    def get_success_url(self):
        return reverse('hiscliapp:vetmascota_detalle', kwargs={'pk': self.object.mascota.pk,})

    def get_form_kwargs(self):
      kwargs = super(VetConsultaModificar, self).get_form_kwargs()
      vetconsulta_id =self.object.pk
      unaconsulta= get_object_or_404(VetConsulta, pk=vetconsulta_id)
      id_clinica = int(unaconsulta.mascota.id_clinica())
      #al modificar, la mascota es un dato de la consulta
      vetmascota_id = unaconsulta.mascota.id

      kwargs.update({
      'selfpk':self.object.pk,
      'modo':'UPD',
      'vetmascota_id':vetmascota_id,
      'id_clinica':id_clinica,
      })
      return kwargs

class VetConsultaBorrar(LoginRequiredMixin,PropietarioMixin,DeleteView):
    model = VetConsulta
    success_url = reverse_lazy('hiscliapp:vetduenio_listar')
    fields = vetconsulta_fields
    
    def delete(self, request, *args, **kwargs):
        vetconsulta = self.get_object()
        id_mascota = vetconsulta.mascota.id
        try:
            vetconsulta.delete()
            estado = 'Consulta eliminada correctamente'
        except ValidationError as e:
            estado = 'La consulta no se puede eliminar. Motivo: ' + str(e)
        respuesta = estado
        return render(request, 'hiscliapp/confirmar_borrado_vetconsulta.html', {"respuesta":respuesta, "vista_render_id_mascota":id_mascota})