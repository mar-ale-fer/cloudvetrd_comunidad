 # -- coding: utf-8 --
from .models import Pais, Provincia, Localidad
from django.http import HttpResponse
from django.core import serializers
import json

def ajax_lista_paises(request):
    qs = Pais.objects.all().order_by('nombre')
    qs_json = serializers.serialize('json', qs)
    #json_encoded = qs_json.encode('utf-8')
    return HttpResponse(qs_json, content_type='application/json')
    
def ajax_lista_provincias(request,id_pais):
    qs = Provincia.objects.all().filter(pais_id=id_pais).order_by('nombre')
    qs_json = serializers.serialize('json', qs)
    #json_encoded = qs_json.encode('utf-8')
    return HttpResponse(qs_json, content_type='application/json')

def ajax_lista_localidades(requeest,id_provincia):
    qs = Localidad.objects.all().filter(provincia__id=id_provincia).order_by('nombre')
    qs_json = serializers.serialize('json', qs)
    #json_encoded = qs_json.encode('utf-8')
    return HttpResponse(qs_json, content_type='application/json')
