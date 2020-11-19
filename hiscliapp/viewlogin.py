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
from datetime import date

from .redigi_decorators import check_recaptcha

from .models import VetPersonal

@csrf_exempt #solo en esta vista desactivar el control de Crsf
@check_recaptcha
def user_login(request):
	#Si el request es HTTP POST, intentar extraer la información relevante
	if request.method == 'POST':
		if request.recaptcha_is_valid:
			#ok seguir
			print('recaptcha valido')
		else:
			context = {"mensaje": "Error en validación 'No soy un robot'"}#Context({"mensaje": "Ha indicado datos de acceso inválidos"})
			return render(request, 'hiscliapp/login.html', context)

		#reunir el usuario y clave provisto por el usuario
		#Se obtiene del form Login.
		username = request.POST.get('username')
		username = username.strip().lower() #quito espacios en blanco
		
		password = request.POST.get('password')
		#consultar a django si la combinación usuario-clave es válida
		#si es válida se retorna un objeto User
		user = authenticate(username=username, password=password)

		#Si no existe el objeto--> no se encontró el usuario con las credenciales indicadas
		request.session['clinica'] = '0' # por defecto no tiene clinica asociada

		if user:
			if user.is_active:
				#Si el usuario es válido y activo, podemos loguearlo
				personal_del_usuario = VetPersonal.objects.get( usuario = user) #busco al personal asociado al usuario
				clinica = personal_del_usuario.clinica
				id_clinica = str(clinica.id)
				clinica_nombre = clinica.nombre
				clinica_imagen = str(clinica.imagen)
				clinica_modo_pago = clinica.modo_pago
				clinica_fin_modo_free = clinica.fecha_fin_free

				print('id clinica:'+ id_clinica+'-')
				login(request,user)

				#Luego del login tengo la sesiòn. La completo con datos
				request.session['clinica'] = id_clinica
				request.session['clinica_nombre'] = clinica_nombre
				request.session['clinica_imagen'] = clinica_imagen
				request.session['clinica_modo_pago'] = clinica_modo_pago
				fin_modo_free_texto = clinica_fin_modo_free.strftime('%d-%m-%Y')				
				request.session['clinica_fin_modo_free'] = fin_modo_free_texto
				#veo si la licencia free ya venció
				hoy = date.today()
				if clinica_modo_pago== 'FREE' and clinica_fin_modo_free < hoy:
					request.session['clinica_habilitada'] = 'rd_falso'
				else:
					request.session['clinica_habilitada'] = 'rd_verdadero'
				#filtros de búsqueda de propietarios
				request.session['lista_vetduenio_filtro_codigo'] = ''
				request.session['lista_vetduenio_filtro_ape'] = ''
				request.session['lista_vetduenio_filtro_nom'] = ''
				request.session['lista_vetduenio_filtro_domicilio'] = ''
				request.session['lista_vetduenio_filtro_email'] = ''
				request.session['lista_vetduenio_filtro_celular_numero'] = ''


				return HttpResponseRedirect( reverse('hiscliapp:vetduenio_listar') )
			else:
				context = {"mensaje": "Su cuenta se encuentra desactivada"} #Context({"mensaje": "Su cuenta se encuentra desactivada"})
				return render(request, 'hiscliapp/login.html', context)
		else:
			context = {"mensaje": "Ha indicado datos de acceso inválidos"}#Context({"mensaje": "Ha indicado datos de acceso inválidos"})
			return render(request, 'hiscliapp/login.html', context)
	else: #Si no es POST, asumo GET y muestro el formulario de Login
		#No paso variables de contexto, así que va el diccionario vacio
		return render(request, 'hiscliapp/login.html',{})

# Use the login_required() decorator to ensure only those logged in can access the view.
#@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    print(request.session)
    request.session['clinica'] = '0'
    print(request.session)
    logout(request)
    # Take the user back to the homepage.
    return HttpResponseRedirect(reverse('hiscliapp:login') )
