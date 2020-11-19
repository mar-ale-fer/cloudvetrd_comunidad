 # -- coding: utf-8 --
from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q #para OR en consultas

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView
localidad_fields = ('nombre')

from .models import Localidad

class LocalidadPrompt(ListView):
    model = Localidad

    template_name = 'hiscliapp/localidad_prompt.html'
    paginate_by = 10

    #búsqueda
    def get_queryset(self):
        filtro_provincia_id = self.request.GET.get('filtro_provincia_id')
        filtro_localidad_nombre = self.request.GET.get('filtro_localidad_nombre')
        qs = Localidad.objects.all()
        
        if not(filtro_provincia_id is None or filtro_provincia_id == ''):
            qs = qs.filter(provincia_id = filtro_provincia_id)
        if not(filtro_localidad_nombre is None or filtro_localidad_nombre == ''):
            qs = qs.filter(nombre__unaccent__icontains= filtro_localidad_nombre) 
        return qs           
    #almacenar contexto de la búsqueda
    def get_context_data(self, **kwargs):
        context = super(LocalidadPrompt, self).get_context_data(**kwargs)
        
        filtro_provincia_id = self.request.GET.get('filtro_provincia_id')
        if filtro_provincia_id: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_provincia_id = filtro_provincia_id.replace(" ","+")
            context['filtro_provincia_id'] = filtro_provincia_id
        
        filtro_localidad_nombre = self.request.GET.get('filtro_localidad_nombre')
        if filtro_localidad_nombre: #si existe el valor, lo agrego/actualizo en el contexto
            filtro_localidad_nombre = filtro_localidad_nombre.replace(" ","+")
            context['filtro_localidad_nombre'] = filtro_localidad_nombre
        return context
