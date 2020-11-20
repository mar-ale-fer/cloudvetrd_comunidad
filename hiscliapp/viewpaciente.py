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

paciente_fields = (
'obra_social',
'numero_afiliado',
'apellido','nombres',
'localidad','domicilio',
'celular_telefonica','celular_numero',
'email','twitter',
'fecha_nacimiento',
'sexo',
)

from .models import Paciente
class DateInput(forms.DateInput):
  input_type = 'date'

class PacienteListar(LoginRequiredMixin, ListView):
    model = Paciente
    paginate_by = 10

    #busqueda
    def get_queryset(self):

        query_ape = self.request.GET.get('filtro_ape')
        query_nom = self.request.GET.get('filtro_nom')
        query_tipo_docu = self.request.GET.get('filtro_tipo_docu')
        query_num_docu = self.request.GET.get('filtro_num_docu')
        query_obra_social = self.request.GET.get('filtro_obra_social')
        query_num_afi = self.request.GET.get('filtro_num_afi')
        qs = Paciente.objects.all().order_by('-id') #antes .all()
        
        #Solo muestra los pacientes creados por el usuario logueado
        usuario_logueado = self.request.user
        qs = qs.filter(creado_por = usuario_logueado)
        
        if not(query_ape is None): #apellido
            qs = qs.filter(apellido__unaccent__icontains= query_ape)
        if not(query_nom is None): #nombre
            qs = qs.filter(nombres__unaccent__icontains= query_nom)
        if not(query_tipo_docu is None): #tipo de documento
            qs = qs.filter(tipo_documento__nombre__icontains= query_tipo_docu)
        if not(query_num_docu is None or query_num_docu == ''): #numero de documento
            qs = qs.filter(numero_documento__icontains=query_num_docu)
        if not(query_obra_social is None): #obra social
            qs = qs.filter(obra_social__nombre__unaccent__icontains= query_obra_social)
        if not(query_num_afi is None or query_num_afi == ''): #numero de afiliado
            qs = qs.filter(numero_afiliado__icontains=query_num_afi)
        return qs
    #almacenar contexto de la busqueda
    def get_context_data(self, **kwargs):
        context = super(PacienteListar, self).get_context_data(**kwargs)
        filtro_ape = self.request.GET.get('filtro_ape')
        if filtro_ape: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_ape = filtro_ape.replace(" ","+")
            context['filtro_ape'] = filtro_ape
        filtro_nom = self.request.GET.get('filtro_nom')
        if filtro_nom: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_nom = filtro_nom.replace(" ","+")
            context['filtro_nom'] = filtro_nom
            
        filtro_tipo_docu = self.request.GET.get('filtro_tipo_docu')
        if filtro_tipo_docu: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_tipo_docu = filtro_tipo_docu.replace(" ","+")
            context['filtro_tipo_docu'] = filtro_tipo_docu
                        
        filtro_num_docu = self.request.GET.get('filtro_num_docu')
        if filtro_num_docu: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_num_docu = filtro_num_docu.replace(" ","+")
            context['filtro_num_docu'] = filtro_num_docu

        filtro_obra_social = self.request.GET.get('filtro_obra_social')
        if filtro_obra_social: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_obra_social = filtro_obra_social.replace(" ","+")
            context['filtro_obra_social'] = filtro_obra_social

        filtro_num_afi = self.request.GET.get('filtro_num_afi')
        if filtro_num_afi: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_num_afi = filtro_num_afi.replace(" ","+")
            context['filtro_num_afi'] = filtro_num_afi

        return context

#Pendiente: Crear Paciente, tomar desde app_encuesta, copiar form y encuesta crear

class PacienteDetalle(LoginRequiredMixin,PropietarioMixin, DetailView):
    model = Paciente
    fields = paciente_fields

class PacienteBorrar(LoginRequiredMixin,PropietarioMixin,DeleteView):
    model = Paciente
    success_url = reverse_lazy('hiscliapp:paciente_listar')
    fields = paciente_fields
    
    def delete(self, request, *args, **kwargs):
        paciente = self.get_object()
        
        try:
            paciente.delete()
            estado = 'Paciente eliminado correctamente'
        except ValidationError as e:
            estado = 'El paciente no se puede eliminar. Motivo: ' + str(e)
        respuesta = estado
        return render(request, 'hiscliapp/confirmar_borrado_paciente.html', {"respuesta":respuesta})
		
			
"""
Crear y modificar
"""
class PacienteForm(ModelForm):
  fecha_nacimiento = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
  def __init__(self, selfpk, modo, *args, **kwargs):

    if modo == 'INS': #al crear activo el prompt
      html_link_paradas = '<a href="#" onclick="showModal();" >Buscar parada</a>'
      html_prompt_paradas = """
          <script type="text/javascript">
            function showModal()
            {
              var dialogWin = window.open('{% url "appencuesta:parada_prompt"  %}', "dialogwidth: 450px; dialogheight: 300px; resizable: yes"); // Showing the Modal Dialog
            }
          </script>
      """
      html_inhabilitar_select = ''
    else:
      html_prompt_paradas = ""
      html_link_paradas = ""
      #al modificar inactivo parada, y momento de encuesta
      html_inhabilitar_select = '' #Desactivado por carga manual
      """ script desactivado:
        <script type="text/javascript">
          $('#id_parada_encuesta option:not(:selected)').attr('disabled',true);
          $('#id_momento option:not(:selected)').attr('disabled',true);
        </script>
      """


    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
        Fieldset('Paciente',
        Row(
        Div('obra_social', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6" ),
        Div('numero_afiliado', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('apellido', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6"),
        Div('nombres', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('tipo_documento', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6"),
        Div('numero_documento', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('localidad', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6"),
        Div('domicilio', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('celular_telefonica', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('celular_numero', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('email', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3 col-md-offset-1 col-lg-offset-1"),
        Div('twitter', css_class="col-xs-12 col-sm-12 col-md-2 col-lg-2"),
        Div('fecha_nacimiento', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6"),
        Div('sexo', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1")
        )),
        FormActions(
          StrictButton('Volver sin guardar',
          onclick="location.href='"+reverse('hiscliapp:paciente_listar',)+"'",
          name="volver",value='volver a lista de pacientes' , css_class="btn-default"),
          Submit('save', 'Guardar', css_class='btn-success'),
        ),
    )
    super(PacienteForm, self).__init__(*args, **kwargs)

  class Meta:
    model = Paciente
    fields = paciente_fields

class PacienteCrear(LoginRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    #fields = paciente_fields

    def get_success_url(self):
        return reverse('hiscliapp:paciente_detalle', kwargs={'pk': self.object.pk,}) #vuelve a lista de encuetas
    def get_form_kwargs(self):
      kwargs = super(PacienteCrear, self).get_form_kwargs()
      kwargs.update({
        'selfpk':0,
        'modo': 'INS'
        }) #pk= 0 todavia no existe
      return kwargs

class PacienteModificar(LoginRequiredMixin,PropietarioMixin, UpdateView):
    model = Paciente
    form_class = PacienteForm

    def get_success_url(self):
        return reverse('hiscliapp:paciente_detalle', kwargs={'pk': self.object.pk}) #va al detalle del paciente

    def get_success_url(self):
        return reverse('hiscliapp:paciente_detalle', kwargs={'pk': self.object.pk,}) #va al detalle del paciente
    def get_form_kwargs(self):
      kwargs = super(PacienteModificar, self).get_form_kwargs()
      kwargs.update({
      'selfpk':self.object.pk,
      'modo':'UPD'
      })
      return kwargs
