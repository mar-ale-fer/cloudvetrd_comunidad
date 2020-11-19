from django.contrib.auth.models import User

from hiscliapp.models import SolicitarAltaClinica
from hiscliapp.models import VetClinica
from hiscliapp.models import VetPersonal
from datetime import date, time, datetime, timedelta
from django.conf import settings

#https://www.geeksforgeeks.org/md5-hash-python/
import hashlib

import smtplib, ssl

#fuente: https://realpython.com/python-send-email/




#fuente background_task
#https://django-background-tasks.readthedocs.io/en/latest/
#ejecutar con $python manage.py process_tasks

#Ejecutar con
#python manage.py runscript hiscliapp_procesos_solicitar_clinica


def run():
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

    print('ejecutado')
    lista_solicitudes = SolicitarAltaClinica.objects.filter(solal_estado = SOLICITADO)

    '''CREAR USUARIO'''
    #https://docs.djangoproject.com/en/2.1/topics/auth/default/#topics-auth-creating-users
    for una_solicitud in lista_solicitudes:
        username = una_solicitud.solal_usuario
        email = una_solicitud.solal_email
        password = una_solicitud.solal_clave
        first_name = una_solicitud.solal_nombre
        last_name = una_solicitud.solal_apellido
        usuario = User.objects.create_user(username=username,
                                 email=email,
                                 password=password)
        usuario.first_name = first_name
        usuario.last_name = last_name
        usuario.save()

        una_solicitud.solal_estado = USUARIO_CREADO
        una_solicitud.save()
        msg_debug='solic:'+str(una_solicitud.id)+', usuario:'+username+' creado'
        print(msg_debug)

    #parahacer: contemplar que un colaborador puede crear su propia clinica
    #que un admin pude nombrar a otro como admin (sin dejar de ser admin)
    #que un usuario existente puede colaborar en más de una clínica
    #ver donde guardar el celular del usuario
    '''CREAR CLÌNICA'''
    siguiente_mes = datetime.now() + timedelta(days=31)
    hoy = date.today()
    MODO_FREE = 'FREE' # $0
    lista_usuario_creado = SolicitarAltaClinica.objects.filter(solal_estado = USUARIO_CREADO)
    for una_solicitud in lista_usuario_creado: 
        nombre_clinica = una_solicitud.solal_nombre_clinica
        
        clinica = VetClinica(nombre=nombre_clinica, 
                    fecha_fin_free = siguiente_mes, 
                    modo_pago= MODO_FREE,
                    fecha_inicio = hoy )
        clinica.save()

        una_solicitud.solal_estado = CLINICA_CREADA
        una_solicitud.save()
        msg_debug='solic:'+str(una_solicitud.id)+', clínica:'+nombre_clinica+' creada'
        print(msg_debug)
    '''ASIGNAR USUARIO A CLINICA'''
    lista_clinica_creada = SolicitarAltaClinica.objects.filter(solal_estado = CLINICA_CREADA)
    for una_solicitud in lista_clinica_creada:
        username= una_solicitud.solal_usuario
        nombre_clinica = una_solicitud.solal_nombre_clinica
        email = una_solicitud.solal_email

        usuario_a_asignar = User.objects.get( username = username) #busco el usuario previamente creado
        print('obtener clinica '+nombre_clinica)
        clinica_a_asignar = VetClinica.objects.get( nombre=nombre_clinica) #busco la clínica previamente creada

        personal_de_clinica = VetPersonal(usuario=usuario_a_asignar,
                                         clinica=clinica_a_asignar,
                                         email= email)
        personal_de_clinica.save()

        una_solicitud.solal_estado = USUARIO_ASIGNADO
        una_solicitud.save()
        msg_debug='solic:'+str(una_solicitud.id)+', usuario:'+username+' asignado a clínica:'+nombre_clinica
        print(msg_debug)      

    '''ASIGNAR HASH PARA TOKEN DE CONFIRMACIÓN DE MAIL'''        
    lista_usuarios_asignados = SolicitarAltaClinica.objects.filter(solal_estado = USUARIO_ASIGNADO)
    for una_solicitud in lista_usuarios_asignados:
        firma = una_solicitud.solal_email.strip() +una_solicitud.solal_clave.strip()
        hashmd5 = hashlib.md5(firma.encode())     
        digest = hashmd5.hexdigest()    
        una_solicitud.solal_token_confirmar_mail = digest
        una_solicitud.save()
        msg_debug='solic:'+str(una_solicitud.id)+', usuario:'+una_solicitud.solal_usuario+'. hash:'+digest
        print(msg_debug)        

    '''ENVIAR MAILS DE BIENVENIDA'''
    port = settings.RD_EMAIL_PORT   # For SSL
    password = settings.RD_EMAIL_HOST_PASSWORD #input("Type your password and press enter: ")
    sender_email = settings.RD_EMAIL_SENDER  
    sender_login = settings.RD_EMAIL_SENDER_LOGIN

    lista_usuarios_asignados = SolicitarAltaClinica.objects.filter(solal_estado = USUARIO_ASIGNADO)
    for una_solicitud in lista_usuarios_asignados:
        token = una_solicitud.solal_token_confirmar_mail
        url_confirmarmail = f'https://cloudvet.respuestadigital.com.ar/hiscliapp/usuario_confirmar_mail/{token}/'

        receiver_email = una_solicitud.solal_email  # Enter receiver address

        
        nombre = una_solicitud.solal_nombre
        usuario = una_solicitud.solal_usuario
        clinica = una_solicitud.solal_nombre_clinica
        message = f"""\
        Subject: {nombre}, Bienvenido a Cloudvet RD

        Ya puedes acceder a administrar tu clínica veterinaria.
        Tus datos de acceso son:
        Usuario: {usuario} 
        Clínica veterinaria: {clinica}

        clic para confirmar mail:{url_confirmarmail}
        
        Atentamente, el equipo de Respuesta Digital
        """
        message = message.encode('utf-8').strip()
        # Create a secure SSL context
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL(settings.RD_EMAIL_HOST, port, context=context) as server:
            server.login(sender_login, password)
            server.sendmail(sender_email, receiver_email, message)

        una_solicitud.solal_estado = MAIL_ENVIADO
        una_solicitud.save()
        msg_debug='solic:'+str(una_solicitud.id)+', usuario:'+usuario+'. mail enviado a:'+receiver_email
        print(msg_debug)        
