from django.shortcuts import render
from .models import PacienteMotivoConsulta, ConsultaImagen
from django.forms.models import inlineformset_factory
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

#Forms
from .form_pacientemotivoconsulta_header import PacienteMotivoConsulta_Header_Form
from .form_consultaimagen import consulta_imagen_InlineFormSet

class admin_consultaimagen(UpdateView):
    template_name= 'hiscliapp/form_consulta_imagen.html'
    model = PacienteMotivoConsulta
    form_class = PacienteMotivoConsulta_Header_Form
    success_url = reverse_lazy('hiscliapp:paciente_listar')
    
    def get_form_kwargs(self):
        kwargs= super(admin_consultaimagen, self).get_form_kwargs()
        kwargs.update({
            'selfpk':self.object.pk,
        })
        return kwargs
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        consulta_form_class = self.get_form_class()
        form = self.get_form(consulta_form_class)
        
        formset = consulta_imagen_InlineFormSet(instance = self.object,
              queryset = (self.object).consultaimagen_set.order_by("fecha_subida") )
        
        return self.render_to_response(
            self.get_context_data(form=form, 
                                  formset=formset ))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        consulta_form_class = self.get_form_class()
        form = self.get_form(consulta_form_class)
        
        formset = consulta_imagen_InlineFormSet(request.POST, request.FILES, 
            instance = self.object)

        print ('form_valid:'+ str(form.is_valid()) + 'formset:' +str(formset.is_valid()))
        
        if formset.is_valid(): #(form.is_valid() and formset.is_valid()):
			#COMENTADO, solo guardo el formset
            #self.object = form.save(commit=False)
            #self.object.save()
            formset.save()
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(form,formset)
        
    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset, form_errors = form.errors))
