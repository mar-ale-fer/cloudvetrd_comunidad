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
from django.contrib.auth.decorators import permission_required
from django.utils.decorators import method_decorator

vetraza_fields = (
'nombre',
)

from .models import VetRaza

class VetRazaListar(LoginRequiredMixin, ListView):
    model = VetRaza
    paginate_by = 10

    #busqueda
    def get_queryset(self):

        query_nom = self.request.GET.get('filtro_nom')
        qs = VetRaza.objects.all().order_by('nombre')

        #+filtro por clinica
        #la clinica del usuario esta en la sesion
        if 'clinica' not in self.request.session:
            id_clinica = 0
        else:
            id_clinica = int(self.request.session['clinica'])
        qs = qs.filter(clinica__id = id_clinica)
        
        #-filtro por clinica        
        #Solo muestra los duenios creados por el usuario logueado
        #usuario_logueado = self.request.user
        #qs = qs.filter(creado_por = usuario_logueado)
        
        if not(query_nom is None): #nombre
            qs = qs.filter(nombre__unaccent__icontains= query_nom)
        return qs
    #almacenar contexto de la busqueda
    def get_context_data(self, **kwargs):
        context = super(VetRazaListar, self).get_context_data(**kwargs)
        
        filtro_nom = self.request.GET.get('filtro_nom')
        if filtro_nom: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_nom = filtro_nom.replace(" ","+")
            context['filtro_nom'] = filtro_nom
        return context

    ''''
    #template para manejo de autorizaciones al grupo
    {% if perms.hiscliapp.ver_raza %}
	    <li><a href="{% url "hiscliapp:vetraza_listar"  %}">Razas</a></li>
	{% endif %}
    @method_decorator(permission_required("hiscliapp.ver_raza"))
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
    '''
class VetRazaDetalle(LoginRequiredMixin, DetailView):
    model = VetRaza
    fields = vetraza_fields

class VetRazaBorrar(LoginRequiredMixin,DeleteView):
    model = VetRaza
    success_url = reverse_lazy('hiscliapp:vetraza_listar')
    fields = vetraza_fields
    
    def delete(self, request, *args, **kwargs):
        vetraza = self.get_object()
        
        try:
            vetraza.delete()
            estado = 'Raza eliminada correctamente'
        except ValidationError as e:
            estado = 'La raza no se puede eliminar. Motivo: ' + str(e)
        respuesta = estado
        return render(request, 'hiscliapp/confirmar_borrado_vetraza.html', {"respuesta":respuesta})
		
			
"""
Crear y modificar
"""
class VetRazaForm(ModelForm):

  def __init__(self, selfpk, modo, *args, **kwargs):

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
        Fieldset('Raza',
        Row(
        Div('nombre', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        )),
        HTML(html_inhabilitar_eliminar),
        FormActions(
          StrictButton('Volver sin guardar',
          onclick="location.href='"+reverse('hiscliapp:vetraza_listar',)+"'",
          name="volver",value='volver a lista de razas' , css_class="btn btn-warning"),

          Submit('save', 'Guardar', css_class='btn-success'),

          StrictButton('Eliminar',
          onclick="location.href='"+"/hiscliapp/vetraza/"+ str(selfpk) +"/borrar/"+ "'",
          id="btn_eliminar",
          name="eliminar",value='eliminar raza' , css_class="btn btn-danger"),  

        ),
    )
    super(VetRazaForm, self).__init__(*args, **kwargs)
    
  class Meta:
    model = VetRaza
    fields = vetraza_fields

class VetRazaCrear(LoginRequiredMixin, CreateView):
    model = VetRaza
    form_class = VetRazaForm
    #fields = paciente_fields

    def get_success_url(self):
        return reverse('hiscliapp:vetraza_listar')
    def get_form_kwargs(self):
      kwargs = super(VetRazaCrear, self).get_form_kwargs()
      kwargs.update({
        'selfpk':0,
        'modo': 'INS'
        }) #pk= 0 todavia no existe
      return kwargs

class VetRazaModificar(LoginRequiredMixin, UpdateView):
    model = VetRaza
    form_class = VetRazaForm

    def get_success_url(self):
        return reverse('hiscliapp:vetraza_listar')

    def get_form_kwargs(self):
      kwargs = super(VetRazaModificar, self).get_form_kwargs()
      kwargs.update({
      'selfpk':self.object.pk,
      'modo':'UPD'
      })
      return kwargs
