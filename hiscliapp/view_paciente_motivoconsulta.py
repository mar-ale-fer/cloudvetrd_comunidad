from django.shortcuts import render
from .models import Paciente, PacienteMotivoConsulta
from django.forms.models import inlineformset_factory
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

#Forms
from .form_paciente_header import Paciente_Header_Form
from .form_paciente_motivoconsulta import motivo_consulta_InlineFormSet


class admin_motivoconsulta(UpdateView):
    template_name= 'hiscliapp/form_paciente_motivoconsulta.html'
    model = Paciente
    form_class = Paciente_Header_Form
    success_url = reverse_lazy('hiscliapp:paciente_listar')
    
    def get_form_kwargs(self):
        kwargs= super(admin_motivoconsulta, self).get_form_kwargs()
        kwargs.update({
            'selfpk':self.object.pk,
        })
        return kwargs
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        paciente_form_class = self.get_form_class()
        form = self.get_form(paciente_form_class)

        
        formset = motivo_consulta_InlineFormSet(instance = self.object,
              queryset = (self.object).pacientemotivoconsulta_set.order_by("fecha") )
        
        return self.render_to_response(
            self.get_context_data(form=form, 
                                  formset=formset ))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        paciente_form_class = self.get_form_class()
        form = self.get_form(paciente_form_class)
        
        formset = motivo_consulta_InlineFormSet(request.POST, request.FILES, 
            instance = self.object)

        print ('form_valid:'+ str(form.is_valid()) + 'formset:' +str(formset.is_valid()))
        
        if formset.is_valid(): #(form.is_valid() and formset.is_valid()):
			#COMENTADO, solo guardo el formset
            #self.object = form.save(commit=False)
            #self.object.save()
            print ('guarda la consulta')
            formset.save()
            #return HttpResponseRedirect(self.get_success_url())
        else:
            #return self.form_invalid(paciente_form, motivo_consulta_form)
            return self.form_invalid(form,formset)
        
    def form_invalid(self, form, formset):
        return self.render_to_response(
            self.get_context_data(form=form, formset=formset, form_errors = form.errors))        

        #return render(request, "hiscliapp/form_paciente_motivoconsulta.html", {"form":form, "formset": formset}) 
