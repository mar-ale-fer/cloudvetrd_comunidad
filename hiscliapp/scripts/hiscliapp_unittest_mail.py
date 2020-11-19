from django.contrib.auth.models import User

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

    '''ENVIAR MAILS DE BIENVENIDA'''
    port = settings.RD_EMAIL_PORT   # For SSL
    password = settings.RD_EMAIL_HOST_PASSWORD #input("Type your password and press enter: ")
    sender_email = settings.RD_EMAIL_SENDER  
    sender_login = settings.RD_EMAIL_SENDER_LOGIN

    token = 'untoken'
    url_confirmarmail = f'https://cloudvet.respuestadigital.com.ar/hiscliapp/usuario_confirmar_mail/{token}/'

    receiver_email = "<redigi>[una cuenta]@gmail.com"  # Enter receiver address

    
    nombre = 'marcelo'
    usuario = 'usuario'
    clinica = 'clinica'
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


    msg_debug=', usuario:'+usuario+'. mail enviado a:'+receiver_email
    print(msg_debug)        
