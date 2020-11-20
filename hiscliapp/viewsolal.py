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
from django.template.loader import get_template

solal_fields = (
'solal_nombre_clinica',
'solal_usuario',
'solal_clave',
'solal_apellido',
'solal_nombre',
'solal_email',
'solal_celular',
)

from hiscliapp.models import SolicitarAltaClinica
from hiscliapp.models import VetClinica
from hiscliapp.models import VetPersonal
from django.contrib.auth.models import User

			
"""
Crear y modificar
"""
class SolicitarAltaClinicaForm(ModelForm):

  solal_clave = forms.CharField(widget=forms.PasswordInput)

  def __init__(self, selfpk,selfcodigo, modo, *args, **kwargs):
    #if modo == 'INS': 
      #html_inhabilitar_select = ''
    #else:
      #html_prompt_paradas = ""      

    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
        Fieldset('Crear una clínica',
        Row(
        Div('solal_nombre_clinica', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('solal_usuario', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('solal_clave', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        #Div('solal_clave', '', placeholder="password", autocomplete='off'),

        Div('solal_apellido', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('solal_nombre', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('solal_email', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('solal_celular', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        )),
        FormActions(
          Submit('save', 'Crear clínica', css_class='btn-success'),
        ),        
    )
    super(SolicitarAltaClinicaForm, self).__init__(*args, **kwargs)
    #self.fields['codigo'].disabled= True
    
  class Meta:
    model = SolicitarAltaClinica
    fields = solal_fields

  def clean(self):
    cleaned_data = super(SolicitarAltaClinicaForm, self).clean()

    solal_nombre_clinica = cleaned_data.get('solal_nombre_clinica')
    solal_usuario = cleaned_data.get('solal_usuario')
    solal_email = cleaned_data.get('solal_email')

    if VetPersonal.objects.filter(email = solal_email).exists():
      if solal_email != '<redigi>[una cuenta de prueba]@gmail.com@gmail.com':
        self.add_error("solal_email", ValidationError('La dirección de email pertenece a otro usuario. Intente con otra dirección de email.'))

    if User.objects.filter(username = solal_usuario).exists():
      self.add_error("solal_usuario", ValidationError('Ya existe el usuario. Intente con otro nombre.'))

    if VetClinica.objects.filter(nombre = solal_nombre_clinica).exists():
      self.add_error("solal_nombre_clinica", ValidationError('Ya existe la clínica. Intente con otro nombre.'))

    # Required only if Django version < 1.7 :
    return cleaned_data

class SolicitarAltaClinicaCrear(CreateView):
    model = SolicitarAltaClinica
    form_class = SolicitarAltaClinicaForm
    #fields = paciente_fields

    def get_success_url(self):
        return reverse('hiscliapp:ag_crear_clinica') #vuelve a lista de encuetas
    def get_form_kwargs(self):
      kwargs = super(SolicitarAltaClinicaCrear, self).get_form_kwargs()
      kwargs.update({
        'selfpk':0,
        'selfcodigo':'',
        'modo': 'INS'
        }) #pk= 0 todavia no existe
      return kwargs