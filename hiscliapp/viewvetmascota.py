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

vetmascota_fields = (
'codigo',
'nombre',
'duenio',
'fecha_nacimiento',
'especie',
'raza','color',
'sexo',
'ultima_consulta',
)

from .models import VetMascota
from .models import VetPersonal
from .models import VetDuenio
from .models import VetRaza

class DateInput(forms.DateInput):
  input_type = 'date'

class VetMascotaListar(LoginRequiredMixin, ListView):
    model = VetMascota
    paginate_by = 10

    #busqueda
    def get_queryset(self):

        query_codigo = self.request.GET.get('filtro_codigo')
        query_nombre = self.request.GET.get('filtro_nombre')
        query_duenio_apellido = self.request.GET.get('filtro_duenio_apellido')
        query_duenio_nombres = self.request.GET.get('filtro_duenio_nombres')
        query_especie = self.request.GET.get('filtro_especie')
        query_raza = self.request.GET.get('filtro_raza')
        query_color = self.request.GET.get('filtro_color')
        query_sexo = self.request.GET.get('filtro_sexo')
        
        qs = VetMascota.objects.all().order_by('id') 

        #+filtro por clinica
        #la clinica del usuario esta en la sesion
        if 'clinica' not in self.request.session:
            id_clinica = 0
        else:
            id_clinica = int(self.request.session['clinica'])
        qs = qs.filter(duenio__clinica__id = id_clinica)
        #-filtro por clinica
        
        if not(query_codigo is None or query_codigo == ''): #codigo de mascota
            qs = qs.filter(codigo__icontains=query_codigo)
        if not(query_nombre is None): 
            qs = qs.filter(nombre__unaccent__icontains= query_nombre) #nombre de mascota    
                    
        if not(query_duenio_apellido is None): #apellido del dueño
            qs = qs.filter(duenio__apellido__unaccent__icontains= query_duenio_apellido)            
        if not(query_duenio_nombres is None): #nombres del dueño
            qs = qs.filter(duenio__nombres__unaccent__icontains= query_duenio_nombres)
            
            
        if not(query_especie is None): #especie código alfanumérico
            qs = qs.filter(especie__unaccent__icontains= query_especie)
        if not(query_raza is None): #raza
            qs = qs.filter(raza__nombre__unaccent__icontains= query_raza)
        if not(query_color is None): #color
            qs = qs.filter(color__unaccent__icontains= query_color)
        if not(query_sexo is None): #sexo
            qs = qs.filter(sexo__unaccent__icontains= query_sexo)
        return qs
    #almacenar contexto de la busqueda
    def get_context_data(self, **kwargs):
        context = super(VetMascotaListar, self).get_context_data(**kwargs)
        
        filtro_codigo = self.request.GET.get('filtro_codigo')
        if filtro_codigo: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_codigo = filtro_codigo.replace(" ","+")
            context['filtro_codigo'] = filtro_codigo
        
        filtro_nombre = self.request.GET.get('filtro_nombre')
        if filtro_nombre: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_nombre = filtro_nombre.replace(" ","+")
            context['filtro_nombre'] = filtro_nombre
            
        filtro_duenio_apellido = self.request.GET.get('filtro_duenio_apellido')
        if filtro_duenio_apellido: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_duenio_apellido = filtro_duenio_apellido.replace(" ","+")
            context['filtro_duenio_apellido'] = filtro_duenio_apellido
 
        filtro_duenio_nombres = self.request.GET.get('filtro_duenio_nombres')
        if filtro_duenio_nombres: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_duenio_nombres = filtro_duenio_nombres.replace(" ","+")
            context['filtro_duenio_nombres'] = filtro_duenio_nombres
                       
        filtro_especie = self.request.GET.get('filtro_especie')
        if filtro_especie: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_especie = filtro_especie.replace(" ","+")
            context['filtro_especie'] = filtro_especie
            
        filtro_raza = self.request.GET.get('filtro_raza')
        if filtro_raza: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_raza = filtro_raza.replace(" ","+")
            context['filtro_raza'] = filtro_raza
            
        filtro_color = self.request.GET.get('filtro_color')
        if filtro_color: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_color = filtro_color.replace(" ","+")
            context['filtro_color'] = filtro_color

        filtro_sexo = self.request.GET.get('filtro_sexo')
        if filtro_sexo: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_sexo = filtro_sexo.replace(" ","+")
            context['filtro_sexo'] = filtro_sexo
        return context



class VetMascotaDetalle(LoginRequiredMixin,PropietarioMixin, DetailView):
    model = VetMascota
    fields = vetmascota_fields

"""
Crear y modificar
"""


class VetMascotaForm(ModelForm):
  fecha_nacimiento = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))

  def __init__(self, selfpk, vetduenio_id, vetduenio_codigo, vetduenio_id_clinica, modo, *args, **kwargs):

    html_focus_nombre = """
        <script type="text/javascript">    
        window.onload = function() {
        document.getElementById("id_nombre").focus();
        };
        </script>
        """      

    if modo == 'INS': 
      html_inhabilitar_algo = ''
    else:
      html_inhabilitar_algo = "" #ver manejo de paradas en sistema de encuesta

    self.helper = FormHelper()
    self.helper.form_class = 'form-horizontal'
    self.helper.form_method = 'post'
    self.helper.layout = Layout(
        Fieldset('Mascota',
        Row(
        Div('codigo', css_class="col-xs-12 col-md-3"),                
        Div('nombre', css_class="col-xs-12 col-sm-12 col-md-8 col-lg-8 col-md-offset-1 col-lg-offset-1"),
        Div('duenio', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('fecha_nacimiento', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('especie', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('raza', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('color', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        Div('sexo', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        HTML(html_focus_nombre),
        )),
        FormActions(
          StrictButton('Volver al propietario',
            #onclick="location.href='"+reverse('hiscliapp:vetduenio_listar',)+"'",
            onclick="location.href='"+"/hiscliapp/vetduenio?filtro_codigo="+ str(vetduenio_codigo) +"'",
            name="volver",value='volver a lista de propietarios' , css_class="btn btn-warning"),
            Submit('save', 'Guardar', css_class='btn-success'),
        ),
    )
    super(VetMascotaForm, self).__init__(*args, **kwargs)
    self.fields['codigo'].disabled= True

    self.fields['duenio'].queryset= VetDuenio.objects.filter(id=vetduenio_id)
    self.fields['duenio'].disabled= True

    #solo mostrar razas de la clínica
    self.fields['raza'].queryset= VetRaza.objects.filter(clinica__id=vetduenio_id_clinica)

  class Meta:
    model = VetMascota
    fields = vetmascota_fields

class VetMascotaCrear(LoginRequiredMixin, CreateView):
    model = VetMascota
    form_class = VetMascotaForm
    #fields = paciente_fields

    def get_success_url(self):
        #return reverse('hiscliapp:vetduenio_detalle', kwargs={'pk': self.object.duenio.pk,}) #vuelve a lista de encuetas
        return reverse('hiscliapp:vetduenio_listar')
    def get_form_kwargs(self):
      kwargs = super(VetMascotaCrear, self).get_form_kwargs()

      vetduenio_id = self.kwargs['vetduenio_id']
      unduenio= get_object_or_404(VetDuenio, pk=vetduenio_id)
      vetduenio_codigo = unduenio.codigo
      vetduenio_id_clinica = unduenio.clinica.id
      kwargs.update({
        'selfpk':0,
        'modo': 'INS',
        'vetduenio_id':vetduenio_id,
        'vetduenio_codigo':vetduenio_codigo,
        'vetduenio_id_clinica':vetduenio_id_clinica,
        }) #pk= 0 todavia no existe
      return kwargs

    def get_initial(self):
        initial = super().get_initial()
        # cpf - it's the name of the field on your current form
        # self.args will be filled from URL. I'd suggest to use named parameters
        # so you can access e.g. self.kwargs['cpf_initial']
        vetduenio_id = self.kwargs['vetduenio_id']
        unduenio= get_object_or_404(VetDuenio, pk=vetduenio_id)
        initial['duenio'] = unduenio


        return initial

class VetMascotaModificar(LoginRequiredMixin,PropietarioMixin, UpdateView):
    model = VetMascota
    form_class = VetMascotaForm

    def get_success_url(self):
        return reverse('hiscliapp:vetmascota_detalle', kwargs={'pk': self.object.pk,}) #va al detalle del paciente
        #return "/hiscliapp/vetduenio?filtro_codigo=" + str(self.object.duenio.codigo)
        #return reverse('hiscliapp:vetduenio_listar')
    def get_form_kwargs(self):
      kwargs = super(VetMascotaModificar, self).get_form_kwargs()
      vetmascota_id =self.object.pk
      unamascota= get_object_or_404(VetMascota, pk=vetmascota_id)


      vetduenio_id = unamascota.duenio.id
      unduenio= get_object_or_404(VetDuenio, pk=vetduenio_id)
      vetduenio_codigo = unduenio.codigo
      vetduenio_id_clinica = unduenio.clinica.id

      kwargs.update({
      'selfpk':self.object.pk,
      'modo':'UPD',
      'vetduenio_id':vetduenio_id,      
      'vetduenio_codigo':vetduenio_codigo,
      'vetduenio_id_clinica':vetduenio_id_clinica,
      })
      return kwargs

class VetMascotaBorrar(LoginRequiredMixin,PropietarioMixin,DeleteView):
    model = VetMascota
    #template de borrado vetmascota_confirm_delete.html
    success_url = reverse_lazy('hiscliapp:vetduenio_listar')
    fields = vetmascota_fields
    
    def delete(self, request, *args, **kwargs):
        vetmascota = self.get_object()
        vetduenio_codigo = vetmascota.duenio.codigo
        eliminado = True
        try:
            vetmascota.delete()
            estado = 'Mascota eliminada correctamente'
            eliminado = True

        except ValidationError as e:
            estado = 'La mascota no se puede eliminar. Motivo: ' + str(e)
            eliminado = False

        respuesta = estado
        return render(request, 'hiscliapp/confirmar_borrado_vetmascota.html', 
        {"respuesta":respuesta,"vetduenio_codigo":vetduenio_codigo,
         "eliminado":eliminado})
		