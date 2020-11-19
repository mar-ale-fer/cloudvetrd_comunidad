# -- coding: utf-8 --
#ver https://docs.djangoproject.com/es/1.9/topics/auth/default/
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse #antes django2 > django.core.urlresolvers import reverse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template import Context

from .models import VetPersonal
from .models import SolicitarAltaClinica

@csrf_exempt #solo en esta vista desactivar el control de Crsf
def usuario_confirmar_mail(request, cloudvet_token):
	#+estados_alta_clinica
	SOLICITADO = 'SOLIC'
	USUARIO_CREADO = 'USU_CREA'
	ERROR_AL_CREAR_USUARIO = 'USU_CREA_ERR'
	CLINICA_CREADA ='CLI_CREA'
	ERROR_AL_CREAR_CLINICA = 'CLI_CREA_ERR'
	USUARIO_ASIGNADO = 'USU_ASI'
	ERROR_ASIGNAR_USUARIO = 'USU_ASI_ERR'
	MAIL_ENVIADO = 'MAIL_ENV'
	MAIL_ERROR = 'MAIL_ERR'
	MAIL_CONFIRMADO = 'MAIL_CONF'
	#-estados_alta_clinica

	#Si el request es HTTP POST, intentar extraer la información relevante
	if request.method == 'GET':
		#reunir el usuario y clave provisto por el usuario
		#Se obtiene del form Login.

		#Si una solicitud coincide con el token
		if SolicitarAltaClinica.objects.filter(solal_token_confirmar_mail = cloudvet_token).exists():
			#modifico la solicitud para indicar que el mail está confirmado
			solicitud_alta = SolicitarAltaClinica.objects.get(solal_token_confirmar_mail=cloudvet_token)
			if solicitud_alta.solal_estado == MAIL_CONFIRMADO:
				context = {"mensaje": "La dirección de mail ya fue confirmada anteriormente",
							"estado": "ok"} 

			else:
				solicitud_alta.solal_estado = MAIL_CONFIRMADO
				solicitud_alta.save()			
				context = {"mensaje": "dirección de mail confirmada",
							"estado": "ok"} 

			return render(request, 'hiscliapp/usuario_confirmar_mail.html',context)

		else:
			context = {"mensaje": "No se pudo confirmar la casilla de email. Consulte a soporte de Cloudvet RD",
						"estado": "error"} 
			return render(request, 'hiscliapp/usuario_confirmar_mail.html',context)


	else: #Si no es GET, asumo POST y muestro el formulario de Login
		#No paso variables de contexto, así que va el diccionario vacio
		context = {"mensaje": "POST. No se pudo confirmar la casilla de email. Consulte a soporte de Cloudvet RD",
					"estado":"error"}
		return render(request, 'hiscliapp/usuario_confirmar_mail.html',context)

