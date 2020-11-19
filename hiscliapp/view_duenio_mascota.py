from django.shortcuts import render
from .models import VetDuenio, VetMascota
from django.forms.models import inlineformset_factory
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.forms import ValidationError
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import PropietarioMixin
#Forms
from .form_vetduenio_header import VetDuenio_Header_Form
from .form_vetduenio_mascota import vetmascota_InlineFormSet


class admin_vetmascota(LoginRequiredMixin,PropietarioMixin,UpdateView):
    template_name= 'hiscliapp/form_vetduenio_vetmascota.html'
    model = VetDuenio
    form_class = VetDuenio_Header_Form
    success_url = reverse_lazy('hiscliapp:vetduenio_listar')
    
    def get_form_kwargs(self):
        kwargs= super(admin_vetmascota, self).get_form_kwargs()
        kwargs.update({
            'selfpk':self.object.pk,
        })
        return kwargs
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        vetduenio_form_class = self.get_form_class()
        form = self.get_form(vetduenio_form_class)

        
        formset = vetmascota_InlineFormSet(instance = self.object,
              queryset = (self.object).vetmascota_set.order_by("nombre") )
        
        return self.render_to_response(
            self.get_context_data(form=form, 
                                  formset=formset ))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        vetduenio_form_class = self.get_form_class()
        form = self.get_form(vetduenio_form_class)
        
        formset = vetmascota_InlineFormSet(request.POST, request.FILES, 
            instance = self.object)

        print ('form_valid:'+ str(form.is_valid()) + 'formset:' +str(formset.is_valid()))
        
        if formset.is_valid(): #(form.is_valid() and formset.is_valid()):
			#COMENTADO, solo guardo el formset
            #self.object = form.save(commit=False)
            #self.object.save()
            print ('guarda la consulta')
            try:
                formset.save()
                return HttpResponseRedirect(self.get_success_url())
            except ValidationError as e:
                estado = 'La mascota no se puede eliminar. Motivo: ' + str(e)
                form.add_error('apellido',estado)
                return self.form_invalid(form,formset)
			    
        else:
            #return self.form_invalid(paciente_form, motivo_consulta_form)
            print ('error en formulario de mascota')
            for unform in formset:
                if not unform.is_valid():
                    print (unform.errors)
            return self.form_invalid(form,formset)
        
    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset, form_errors = form.errors))        

        #return render(request, "hiscliapp/form_paciente_motivoconsulta.html", {"form":form, "formset": formset}) 
