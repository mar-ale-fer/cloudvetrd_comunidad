from django.shortcuts import render
from .models import Paciente, AntecedentesFamiliares
from django.forms.models import inlineformset_factory
from django.views.generic import UpdateView
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect

#Forms
from .form_paciente_header import Paciente_Header_Form
from .form_antecedentesfamiliares import antecedentes_familiares_InlineFormSet

class admin_antecedentesfamiliares(UpdateView):
    template_name= 'hiscliapp/form_antecedentes_familiares.html'
    model = Paciente
    form_class = Paciente_Header_Form
    success_url = reverse_lazy('hiscliapp:paciente_listar')
    
    def get_form_kwargs(self):
        kwargs= super(admin_antecedentesfamiliares, self).get_form_kwargs()
        kwargs.update({
            'selfpk':self.object.pk,
        })
        return kwargs
    
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        paciente_form_class = self.get_form_class()
        form = self.get_form(paciente_form_class)

        formset = antecedentes_familiares_InlineFormSet(instance = self.object,
              queryset = AntecedentesFamiliares.objects.filter(paciente__id = (self.object.id)) )#onetoone usa select_related
        #queryset = (self.object).antecedentesfamiliares )#onetoone usa select_related
        
        return self.render_to_response(
            self.get_context_data(form=form, 
                                  formset=formset ))
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        paciente_form_class = self.get_form_class()
        form = self.get_form(paciente_form_class)
        
        formset = antecedentes_familiares_InlineFormSet(request.POST, request.FILES, 
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
