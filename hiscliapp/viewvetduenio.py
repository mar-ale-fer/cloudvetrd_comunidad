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

vetduenio_fields = (
'codigo',
'apellido','nombres',
'codigo',
'domicilio',
'celular_numero',
'email',
'observaciones'
)

from .models import VetDuenio
from .models import VetPersonal

class DateInput(forms.DateInput):
  input_type = 'date'

class VetDuenioListar(LoginRequiredMixin, ListView):
    model = VetDuenio
    paginate_by = 10

    #busqueda
    def get(self, *args, **kwargs):

        #Si ya expiró el período free, lo debe registrar en la sesión.
        #evitar altas y modificaciones de datos de:
        #propietarios, sus mascotas, consultas.

        query_codigo = self.request.GET.get('filtro_codigo')
        query_ape = self.request.GET.get('filtro_ape')
        query_nom = self.request.GET.get('filtro_nom')
        query_domicilio = self.request.GET.get('filtro_domicilio')
        query_email = self.request.GET.get('filtro_email')
        query_celular_numero = self.request.GET.get('filtro_celular_numero')

        if not(query_codigo is None):
            self.request.session['lista_vetduenio_filtro_codigo'] = query_codigo
        if not(query_ape is None):
            self.request.session['lista_vetduenio_filtro_ape'] = query_ape
        if not(query_nom is None):
            self.request.session['lista_vetduenio_filtro_nom'] = query_nom
        if not(query_domicilio is None):
            self.request.session['lista_vetduenio_filtro_domicilio'] = query_domicilio
        if not(query_email is None):
            self.request.session['lista_vetduenio_filtro_email'] = query_email
        if not(query_celular_numero is None):
            self.request.session['lista_vetduenio_filtro_celular_numero'] = query_celular_numero

        resp = super().get(*args, **kwargs)
        return resp

    def get_queryset(self):
        query_codigo = self.request.session['lista_vetduenio_filtro_codigo']
        query_ape = self.request.session['lista_vetduenio_filtro_ape']
        query_nom = self.request.session['lista_vetduenio_filtro_nom']
        query_domicilio = self.request.session['lista_vetduenio_filtro_domicilio']
        query_email = self.request.session['lista_vetduenio_filtro_email']
        query_celular_numero = self.request.session['lista_vetduenio_filtro_celular_numero']

        qs = VetDuenio.objects.all().order_by('-id') #antes .all()
                
        #+filtro por clinica
        #la clinica del usuario esta en la sesion
        if 'clinica' not in self.request.session:
            id_clinica = 0
        else:
            id_clinica = int(self.request.session['clinica'])
        qs = qs.filter(clinica__id = id_clinica)
        #-filtro por clinica
        
        if not(query_codigo is None or query_codigo == ''): #codigo de dueño
            qs = qs.filter(codigo__icontains=query_codigo)
        if not(query_ape is None or query_ape == ''): #apellido
            qs = qs.filter(apellido__unaccent__icontains= query_ape)
        if not(query_nom is None or query_nom == ''): #nombre
            qs = qs.filter(nombres__unaccent__icontains= query_nom)
        if not(query_domicilio is None or query_domicilio== '' ): #domicilio
            qs = qs.filter(domicilio__unaccent__icontains= query_domicilio)
        if not(query_email is None or query_email == ''): #email
            qs = qs.filter(email__unaccent__icontains= query_email) 
        if not(query_celular_numero is None or query_celular_numero == ''): #numero de celular
            qs = qs.filter(celular_numero__unaccent__icontains= query_celular_numero)            
        return qs
    #almacenar contexto de la busqueda
    def get_context_data(self, **kwargs):
        context = super(VetDuenioListar, self).get_context_data(**kwargs)
        

        
        filtro_codigo = self.request.session['lista_vetduenio_filtro_codigo']
        filtro_ape = self.request.session['lista_vetduenio_filtro_ape']
        filtro_nom = self.request.session['lista_vetduenio_filtro_nom']
        filtro_domicilio = self.request.session['lista_vetduenio_filtro_domicilio']
        filtro_email = self.request.session['lista_vetduenio_filtro_email']
        filtro_celular_numero = self.request.session['lista_vetduenio_filtro_celular_numero']

        if filtro_codigo: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_codigo = filtro_codigo.replace(" ","+")
            context['filtro_codigo'] = filtro_codigo
        
        if filtro_ape: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_ape = filtro_ape.replace(" ","+")
            context['filtro_ape'] = filtro_ape

        if filtro_nom: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_nom = filtro_nom.replace(" ","+")
            context['filtro_nom'] = filtro_nom
            
        if filtro_domicilio: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_domicilio = filtro_domicilio.replace(" ","+")
            context['filtro_domicilio'] = filtro_domicilio

        if filtro_email: 
            filtro_email = filtro_email.replace(" ","+")
            context['filtro_email'] = filtro_email
            
        if filtro_celular_numero: 
            filtro_celular_numero = filtro_celular_numero.replace(" ","+")
            context['filtro_celular_numero'] = filtro_celular_numero            
        return context

class VetDuenioDetalle(LoginRequiredMixin,PropietarioMixin, DetailView):
    model = VetDuenio
    fields = vetduenio_fields

class VetDuenioMascotasDetalle(LoginRequiredMixin,PropietarioMixin, DetailView):
    template_name = 'hiscliapp/vetduenio_mascotas_detail.html'
    model = VetDuenio
    fields = vetduenio_fields

class VetDuenioBorrar(LoginRequiredMixin,PropietarioMixin,DeleteView):
    model = VetDuenio
    #template de borrado vetduenio_confirm_delete.html
    success_url = reverse_lazy('hiscliapp:vetduenio_listar')
    fields = vetduenio_fields
    
    def delete(self, request, *args, **kwargs):
        vetduenio = self.get_object()
        vetduenio_codigo = vetduenio.codigo
        eliminado = True

        try:
            vetduenio.delete()
            estado = 'Propietario eliminado correctamente'
            eliminado = True

        except ValidationError as e:
            estado = 'El propietario no se puede eliminar. Motivo: ' + str(e)
            eliminado = False

        respuesta = estado
        return render(request, 'hiscliapp/confirmar_borrado_vetduenio.html', 
        {"respuesta":respuesta,"vetduenio_codigo":vetduenio_codigo,
         "eliminado":eliminado})
		
			
"""
Crear y modificar
"""
class VetDuenioForm(ModelForm):
  #fecha_nacimiento = forms.DateField(widget=forms.TextInput(attrs={'type':'date'}))
  observaciones = forms.CharField(widget=forms.Textarea(attrs={'rows':2}))
  
  def __init__(self, selfpk,selfcodigo, modo, *args, **kwargs):

    #html_link_localidades = """
    #<div class="col-xs-6 col-sm-6 col-md-3 col-lg-3"> 
    #  <a href="#" onclick="showModal();" >Buscar localidad</a>    
    #</div>
    #
    #"""
    html_focus_apellido = """
        <script type="text/javascript">    
        window.onload = function() {
        document.getElementById("id_apellido").focus();
        };
        </script>
        """

    html_prompt_localidades = """
          <script type="text/javascript">
            function showModal()
            {
                //var dialogWin = window.open('{% url "hiscliapp:localidad_prompt"  %}', "dialogwidth: 450px; dialogheight: 300px; resizable: yes"); // Showing the Modal Dialog
                //fuente:https://javascript.info/popup-windows
                let params = `scrollbars=yes,resizable=yes,status=no,location=no,toolbar=no,menubar=no,
                width=800,height=600,left=200,top=100`;

                var dialogWin = window.open('{% url "hiscliapp:localidad_prompt"  %}', 'test', params);                
                //var dialogWin = window.showModalDialog('{% url "hiscliapp:localidad_prompt"  %}', 'test', params);   
                dialogWin.focus(); 

                //pongo en gris la ventana llamadora
                document.getElementById('blackout').style.display = 'block';   

                //si sale del prompt, este se cierra
                dialogWin.onblur = function() { 
                    dialogWin.close(); 
                    document.getElementById('blackout').style.display = 'none';
                };          
            }
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
        Fieldset('Propietario',
        Row(
        Div('codigo', css_class="col-xs-12 col-md-3"),                
        Div('apellido', css_class="text-capitalize col-xs-12 col-sm-12 col-md-9 col-lg-9"),
        Div('nombres', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        
        #HTML("""
        #<div class="col-xs-12 col-xm-12 col-md-12 col-lg-12">
        #<button type="button" class="btn btn-info" data-toggle="collapse" data-target="#documento">Documento (opcional)</button>
        #</div>
        #"""),
        #HTML('<div id="documento" class="col-xs-12 col-xm-12 col-md-12 col-lg-12 collapse">'),
        #  Div('tipo_documento', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6"),
        #  Div('numero_documento', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        #HTML('</div>'),
        #Div('localidad', css_class="col-xs-6 col-sm-6 col-md-3 col-lg-3"),
        #HTML(html_link_localidades),
        HTML(html_focus_apellido),
        Div('domicilio', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),
        #Div('celular_telefonica', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('celular_numero', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3"),
        Div('email', css_class="col-xs-12 col-sm-12 col-md-3 col-lg-3 col-md-offset-1 col-lg-offset-1"),
        Div('observaciones', css_class="col-xs-12 col-sm-12 col-md-12 col-lg-12 col-md-offset-1 col-lg-offset-1"),
        #Div('twitter', css_class="col-xs-12 col-sm-12 col-md-2 col-lg-2"),
        #Div('feselfpkcha_nacimiento', css_class="col-xs-12 col-sm-12 col-md-6 col-lg-6"),
        #Div('cuit', css_class="col-xs-12 col-sm-12 col-md-5 col-lg-5 col-md-offset-1 col-lg-offset-1"),        
        )),
        FormActions(
          Submit('save', 'Guardar', css_class='btn-success'),

          StrictButton('Volver sin guardar',
          #onclick="location.href='"+reverse('hiscliapp:vetduenio_listar',)+"'",
          onclick="location.href='"+"/hiscliapp/vetduenio/"+ "'",
          name="volver",value='volver a lista de propietarios' , css_class="btn btn-warning"),


          StrictButton('Eliminar',
          onclick="location.href='"+"/hiscliapp/vetduenio/"+ str(selfpk) +"/borrar/"+ "'",
          id="btn_eliminar",
          name="eliminar",value='eliminar propietario' , css_class="btn btn-danger"),  

        ),
        #HTML(html_prompt_localidades),
        HTML(html_inhabilitar_eliminar),
    )
    super(VetDuenioForm, self).__init__(*args, **kwargs)
    self.fields['codigo'].disabled= True
  class Meta:
    model = VetDuenio
    fields = vetduenio_fields

class VetDuenioCrear(LoginRequiredMixin, CreateView):
    model = VetDuenio
    form_class = VetDuenioForm
    #fields = paciente_fields

    def get_success_url(self):
        #return "/hiscliapp/vetduenio?filtro_codigo="+self.object.codigo
        return reverse_lazy('hiscliapp:vetduenio_listar')


    def get_form_kwargs(self):
      kwargs = super(VetDuenioCrear, self).get_form_kwargs()
      kwargs.update({
        'selfpk':0,
        'selfcodigo':'',
        'modo': 'INS'
        }) #pk= 0 todavia no existe
      return kwargs

class VetDuenioModificar(LoginRequiredMixin,PropietarioMixin, UpdateView):
    model = VetDuenio
    form_class = VetDuenioForm

    def get_success_url(self):
        #return reverse('hiscliapp:vetduenio_detalle', kwargs={'pk': self.object.pk,}) #va al detalle del paciente
        return reverse_lazy('hiscliapp:vetduenio_listar')

    def get_form_kwargs(self):
      kwargs = super(VetDuenioModificar, self).get_form_kwargs()
      kwargs.update({
      'selfpk':self.object.pk,
      'selfcodigo':self.object.codigo,
      'modo':'UPD'
      })
      return kwargs
