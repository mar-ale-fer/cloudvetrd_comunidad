# -- coding: utf-8 --
from django.db import models
from datetime import date, time, datetime, timedelta

from django.db.models.query import QuerySet
from django.core.validators import RegexValidator
from django.forms import ValidationError 
from django.db.models import Max
from crum import get_current_user
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.db.models import Q

alphanumeric_validator = RegexValidator(r'^[0-9a-zA-Z]*$', 'Son permitidos solo caracteres alfanuméricos')
numeric_validator = RegexValidator(r'^[0-9]*$', 'Son permitidos solo caracteres numéricos')

class Numerador (models.Model):
	nombre = models.CharField(max_length=30, blank='true',unique=True)
	ultimo_valor = models.IntegerField(default=0)
	def __str__(self):
		return self.nombre

def sigNumero(nombreNumerador):
	try:
		n = Numerador.objects.get(nombre=nombreNumerador)
	except Numerador.DoesNotExist:
		#Si no existe en la BD, lo creo
		n = Numerador(nombre=nombreNumerador, ultimo_valor = 1)
		n.save()
		return n.ultimo_valor
	else:
		#si existe, incremento el valor, lo guardo y lo retorno
		n.ultimo_valor += 1
		n.save()
		return n.ultimo_valor

def completarConCeros( numero, longitud):
	numerotxt = str(numero)
	return numerotxt.zfill(longitud)

class PropietarioMixin(object):
    """
    Mixin providing a dispatch overload that checks object ownership. is_staff and is_supervisor
    are considered object owners as well. This mixin must be loaded before any class based views
    are loaded for example class SomeView(OwnershipMixin, ListView)
    """
    def dispatch(self, request, *args, **kwargs):
        self.request = request
        self.args = args
        self.kwargs = kwargs
        # we need to manually "wake up" self.request.user which is still a SimpleLazyObject at this point
        # and manually obtain this object's owner information.
        current_user = get_current_user() # self.request.user._wrapped if hasattr(self.request.user, '_wrapped') else self.request.user
        #object_owner = getattr(self.get_object(), 'creado_por')
        
        self.object = self.get_object()
        object_id_clinica =  self.object.id_clinica()
        
        print(self.object)
        print(object_id_clinica)
        #la clinica del usuario esta en la sesion
        if 'clinica' not in self.request.session:
            id_clinica = 0
        else:
            id_clinica = int(self.request.session['clinica'])        
        
        #if current_user != object_owner and not current_user.is_superuser and not current_user.is_staff:
        #    raise PermissionDenied
        
        if id_clinica != object_id_clinica and not current_user.is_superuser and not current_user.is_staff:
            raise PermissionDenied
        return super(PropietarioMixin, self).dispatch(request, *args, **kwargs)

class Pais (models.Model):
    nombre = models.CharField('Nombre del país', max_length= 50)
    prefijo_telefonico = models.CharField('Prefijo telefónico (incluido el +)', max_length= 4) 
    def __str__(self):
        return self.nombre
    class Meta:
        verbose_name="País"
        verbose_name_plural="Paises"

class Provincia (models.Model):
    nombre = models.CharField('Nombre de la provincia', max_length= 50)
    pais = models.ForeignKey(Pais, verbose_name='País', on_delete = models.PROTECT)
    def __str__(self):
        return self.pais.prefijo_telefonico +'-'+ self.nombre

class Localidad (models.Model):
    nombre = models.CharField('Nombre de la localidad', max_length= 50)
    provincia = models.ForeignKey(Provincia, verbose_name='Provincia', on_delete = models.PROTECT)
    def __str__(self):
        return self.nombre +'. '+self.provincia.nombre
    class Meta:
        verbose_name="Localidad"
        verbose_name_plural="Localidades"

class TipoDocumento (models.Model):
    nombre = models.CharField('Nombre del tipo de documento', max_length= 20) #Ejemplo AR-DNI
    pais = models.ForeignKey(Pais, verbose_name='País', on_delete = models.PROTECT)
    def __str__(self):
        #return self.pais.prefijo_telefonico +'-'+self.nombre
        return self.nombre
    class Meta:
        verbose_name="Tipo de documento"
        verbose_name_plural="Tipos de documento"

class Persona (models.Model):
    apellido = models.CharField('Apellido', max_length= 128)
    nombres = models.CharField('Nombres', max_length= 128)
    #tipo_documento = models.ForeignKey(TipoDocumento, verbose_name='Tipo de documento', on_delete = models.PROTECT, blank=True, null=True, default=None)
    #numero_documento = models.CharField('Número de documento', max_length= 15, blank='true', validators=[numeric_validator]) #sólo números
    #localidad = models.ForeignKey(Localidad, verbose_name='Localidad', on_delete = models.PROTECT)
    domicilio = models.CharField('Domicilio', max_length= 128)
    celular_numero = models.CharField('Número de celular', max_length= 30,null='true', blank='true')
    email = models.EmailField('dirección de e-mail',null='true', blank='true')
    #twitter = models.CharField('cuenta de twitter', max_length= 50,null='true', blank='true')
    #fecha_nacimiento = models.DateField('dia y mes de cumpleaños', default=date.today)
    class Meta:
        verbose_name="Persona"
        verbose_name_plural="Personas"

#----veterinaria

class VetClinica (models.Model):
    MODO_FREE = 'FREE' # $0
    MODO_STARTER = 'STARTER' # $3 por 6 meses
    MODO_STANDARD = 'STANDARD' #5 por mes 
    MODO_PREMIUM = 'PREMIUM' # $8 por mes, incluye informe estadístico trimestral
    MODO_PAGO = (
        (MODO_FREE, 'Modo Free'),
        (MODO_STARTER, 'Modo Starter'),
        (MODO_STANDARD, 'Modo Standard'),
        (MODO_PREMIUM, 'Modo Premium'),
    )
    nombre = models.CharField('Nombre', max_length= 128)
    imagen = models.ImageField(upload_to = 'consultas/%Y/%m/%d/', default='consultas/vacio/imagenvacia.jpg')
    fecha_alta = models.DateField('Fecha de alta', default= date.today, null='true', blank='true')
    fecha_fin_free = models.DateField('Fin del modo Free', default=date.today, null='true', blank='true')
    modo_pago = models.CharField('Modo de pago',max_length=8, choices=MODO_PAGO)
    fecha_inicio = models.DateField('Fecha de alta', default=date.today, null='true', blank='true')
    def __str__(self):
        return self.nombre
        		
    class Meta:
        verbose_name="Clínica veterinaria"
        verbose_name_plural="Clínicas veterinarias"	

class VetPersonal (models.Model):
    usuario = models.ForeignKey(User, on_delete = models.PROTECT) 
    clinica = models.ForeignKey(VetClinica, verbose_name='Clínica', on_delete = models.PROTECT, blank=True, null=True, default=None)
    email = models.EmailField('e-mail',blank=True, null=True, default=None)
    
    def __str__(self):
        return self.usuario.get_full_name()#self.usuario.first_name
        		
    class Meta:
        verbose_name="Personal"
        verbose_name_plural="Personal"	

    def save(self, *args, **kwargs):        
        if not self.pk: #si no tiene pk, es insert
            id_actual=0
        else:
            id_actual= self.pk
        
        if VetPersonal.objects.filter(email = self.email).exclude(id = id_actual).exists():
            #para debug
            if self.email != '<redigi>[una cuenta de prueba]@gmail.com@gmail.com':
                raise ValidationError('La dirección de email pertenece a otro usuario. Intente con otra dirección de email')

        super(VetPersonal, self).save(*args, **kwargs)

class VetDuenio (Persona):
    codigo = models.CharField('Código',max_length=10,blank='true') #autoincremental	
    observaciones = models.TextField('Observaciones', max_length= 528 )
    creado = models.DateTimeField(auto_now_add=True, blank= True)
    creado_por = models.ForeignKey('auth.User', related_name= 'Propietario_creado_por', blank=True, null=True, default=None,on_delete = models.PROTECT)
    modificado = models.DateTimeField(auto_now=True, blank = True)
    modificado_por = models.ForeignKey('auth.User', related_name= 'Propietario_modificado_por',blank=True, null=True, default=None,on_delete = models.PROTECT)
    ultima_mascota = models.IntegerField(default=0)
    clinica = models.ForeignKey(VetClinica, related_name= 'Propietario_pertenece_a',blank=True, null=True, default=None,on_delete = models.PROTECT)
    def save(self, *args, **kwargs):
        usuario = get_current_user()
        if usuario and not usuario.pk:
            usuario = None
        #el usuario vacio se utiliza en la migración, si está vacio dejo avanzar y lo completo luego
        if usuario:
            if not self.pk: #si todavía no tiene pk, es insert
                self.codigo = completarConCeros( sigNumero('NUMPROPIETARIO'), 5) #asigno el numerador actual dentro de la campaña			
                self.creado_por = usuario
                #asocio al propietario con la clinica del usuario logueado
                personal_del_usuario = VetPersonal.objects.get( usuario = usuario) #busco al personal asociado al usuario
                self.clinica = personal_del_usuario.clinica #asigno la clinica, para visibilida
                
                #self.ultima_consulta = self.creado.date() #la última consulta coincide con la creación
            self.modificado_por = usuario #cada vez que se modifica, o al insertar 
        #Paso a mayúscula la primera letra de cada palabra       
        self.apellido = self.apellido.title() 
        self.nombres = self.nombres.title()
        super(VetDuenio, self).save(*args, **kwargs)
    def __str__(self):
        return self.apellido +', '+ self.nombres
    class Meta:
        verbose_name = 'Propietario'
    def delete(self, *args, **kwargs):
        if VetMascota.objects.filter(duenio__pk = self.pk).exists():
            raise ValidationError('El propietario tiene mascotas cargadas.')
        super(VetDuenio, self).delete(*args, **kwargs)
    def id_clinica(self):
        return self.clinica.id

class VetRaza (models.Model):
    nombre = models.CharField('Nombre', max_length= 128)
    creado = models.DateTimeField(auto_now_add=True, blank= True, null=True)
    creado_por = models.ForeignKey('auth.User', related_name= 'Raza_creada_por', blank=True, null=True, default=None,on_delete = models.PROTECT)
    modificado = models.DateTimeField(auto_now=True, blank = True, null=True)
    modificado_por = models.ForeignKey('auth.User', related_name= 'Raza_modificada_por',blank=True, null=True, default=None,on_delete = models.PROTECT)
    clinica = models.ForeignKey(VetClinica, related_name= 'Raza_pertenece_a',blank=True, null=True, default=None,on_delete = models.PROTECT)
	
    def __str__(self):
        return self.nombre
		
    def save(self, *args, **kwargs):
        usuario = get_current_user()
        if usuario and not usuario.pk:
            usuario = None

        #el usuario vacio se utiliza en la migración, si está vacio dejo avanzar y lo completo luego
        if usuario:
            if not self.pk: #si todavía no tiene pk, es insert
                self.creado_por = usuario
                self.modificado_por = usuario #cada vez que se modifica, o al insertar
                personal_del_usuario = VetPersonal.objects.get( usuario = usuario) #busco al personal asociado al usuario
                self.clinica = personal_del_usuario.clinica #asigno la clinica, para visibilida

        super(VetRaza, self).save(*args, **kwargs)
        		
    class Meta:
        verbose_name="Raza"
        verbose_name_plural="Razas"
        permissions = (
            ("ver_raza", "Acceso a Razas"),
        )

    def delete(self, *args, **kwargs):
        if VetMascota.objects.filter(raza__pk = self.pk).exists():
            raise ValidationError('Hay mascotas cargadas con la raza que intenta eliminar.')
        super(VetRaza, self).delete(*args, **kwargs)
    def id_clinica(self):
        return self.clinica.id
	
class VetMascota (models.Model):
    FEMENINO = 'F'
    MASCULINO = 'M'
    
    SEXO_BIOLOGICO = (
        (FEMENINO, 'Hembra'),
        (MASCULINO, 'Macho'),
    )
    PERRO = 'PER'
    GATO = 'GAT'
    IGUANA = 'IGU'
    TORTUGA = 'TOR'
    CONEJO = 'CON'
    CERDO = 'CER'
    CABRA = 'CAB'
    AVE = 'AVE'
    ESPECIE = (
        (PERRO, 'Perro'),
        (GATO, 'Gato'),
        (IGUANA, 'Iguana'),
        (TORTUGA, 'Tortuga'),
        (CONEJO, 'Conejo'),
        (CERDO, 'Cerdo'),
        (CABRA, 'Cabra'),
        (AVE, 'Ave'),
    )
    codigo = models.CharField('Código',max_length=10,blank='true') #autoincremental dentro del dueño	
    nombre = models.CharField('Nombre', max_length= 128)
    duenio =  models.ForeignKey(VetDuenio, verbose_name='Propietario', on_delete = models.PROTECT)    
    fecha_nacimiento = models.DateField('Fecha de nacimiento', default=date.today)
    especie = models.CharField('Especie',max_length=3, choices=ESPECIE)
    raza = models.ForeignKey(VetRaza, verbose_name='Raza', on_delete = models.PROTECT, blank=True, null=True, default=None)
    color = models.CharField('Color', max_length= 80)
    sexo = models.CharField('Sexo',max_length=1, choices=SEXO_BIOLOGICO)
    ultima_consulta = models.DateField('Última consulta', default=date.today,null='true', blank='true') #por defecto la última consulta coincide con la fecha de creación
    def __str__(self):
        return self.especie + '-'+ self.nombre
    class Meta:
        verbose_name="Mascota"
        verbose_name_plural="Mascotas" 
    def delete(self, *args, **kwargs):
        if VetConsulta.objects.filter(mascota__pk = self.pk).exists():
            raise ValidationError('La mascota {} tiene consultas cargadas.'.format(self.nombre))
        super(VetMascota, self).delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if not self.pk: #si no tiene pk, es insert
            #incremento ultima_mascota del dueño
            id_duenio = self.duenio.id
            duenio_de_mascota = VetDuenio.objects.get( pk = id_duenio)
            duenio_de_mascota.ultima_mascota +=1 #incremento la ultima mascota
            nuevo_id_mascota = duenio_de_mascota.ultima_mascota
		    
            duenio_de_mascota.save()
            #asigno el id de mascota
            self.codigo = duenio_de_mascota.codigo +'/'+ (str(nuevo_id_mascota)).strip()
        self.nombre = self.nombre.title()
        super(VetMascota, self).save(*args, **kwargs)
    def id_clinica(self):
        return self.duenio.clinica.id         

class VetMotivoConsulta (models.Model):
    ADEMANDA = 'DEM'
    PROGRAMADA = 'PRO'
    EMERGENCIA = 'EME'

    TIPO_CONSULTA = (
        (ADEMANDA, 'A demanda'),
        (PROGRAMADA, 'Programada'),
        (EMERGENCIA, 'Emergencia'),
    )
    nombre = models.CharField('Nombre del motivo de consulta', max_length= 50)
    tipo = models.CharField('tipo de motivo de consulta',max_length=3, choices=TIPO_CONSULTA)
    
    def __str__(self):
        return self.tipo + '-'+ self.nombre
    class Meta:
        verbose_name="Motivo de consulta"
        verbose_name_plural="Motivos de consulta"   

class VetConsulta (models.Model):
    mascota =  models.ForeignKey(VetMascota, verbose_name='Mascota', on_delete = models.PROTECT)
    fecha = models.DateField('Fecha de consulta', default=date.today)
    motivo_consulta =  models.ForeignKey(VetMotivoConsulta, verbose_name='Motivo de consulta', on_delete = models.PROTECT)
    peso = models.DecimalField('Peso en Kg',max_digits=7,decimal_places=3, blank='true', default=0)
    observaciones = models.TextField('Observaciones', max_length= 528 )
    cuenta_corriente = models.DecimalField('Cuenta corriente $ ',default= 0,max_digits=7,decimal_places=2)
    atendio = models.ForeignKey(VetPersonal, verbose_name='Atendió',related_name='Personal_que_atendio', blank=True, null=True, default=None, on_delete = models.PROTECT)
    
    def __str__(self):
        return self.motivo_consulta.nombre + '- fecha:' + '{:%d/%m/%Y}'.format(self.fecha)
    class Meta:
        verbose_name="Consulta de la mascota"
        verbose_name_plural="Consultas de la mascota" 
         
    def save(self, *args, **kwargs):
        #actualizo la última consulta en el paciente
        id_mascota = self.mascota.id
        mascota_de_consulta = VetMascota.objects.get( pk = id_mascota) #busco al paciente entre las mascotas
        mascota_de_consulta.ultima_consulta = self.fecha
        mascota_de_consulta.save()
        super(VetConsulta, self).save(*args, **kwargs)
    def id_clinica(self):
        return self.mascota.duenio.clinica.id            

class VetConsultaImagen (models.Model):
    consulta = models.ForeignKey(VetConsulta, verbose_name='Consulta', on_delete = models.PROTECT)
    imagen = models.ImageField(upload_to = 'consultas/%Y/%m/%d/', default='consultas/vacio/imagenvacia.jpg')
    fecha_subida = models.DateTimeField(auto_now_add=True)



class SolicitarAltaClinica (models.Model):
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

    ESTADO_CREAR_CLINICA = (
        (SOLICITADO, 'Solicitado'),
        (USUARIO_CREADO, 'Usuario creado'),
        (ERROR_AL_CREAR_USUARIO, 'Error al crear usuario'),
        (CLINICA_CREADA, 'Clínica creada'),
        (ERROR_AL_CREAR_CLINICA, 'Error al crear clínica'),
        (USUARIO_ASIGNADO,'Usuario asignado a la clínica'),
        (ERROR_ASIGNAR_USUARIO,'Error al asignar usuario a la clinica'),
        (MAIL_ENVIADO, 'Mail enviado ok, luego de crear clínica'),
        (MAIL_ERROR, 'Error al enviar mail'),
        (MAIL_CONFIRMADO, 'Casilla de correo confirmada por el usuario'),
    )

    solal_nombre_clinica =  models.CharField('Nombre de la clínica', max_length= 128)
    solal_usuario = models.CharField('Usuario', max_length= 50)
    solal_clave = models.CharField('Clave', max_length= 50)
    solal_apellido =  models.CharField('Apellido', max_length= 128)
    solal_nombre = models.CharField('Nombre', max_length= 128)
    solal_email = models.EmailField('dirección de e-mail',)
    solal_celular = models.CharField('Número de celular', max_length= 30,null='true', blank='true')
    solal_estado = models.CharField('Estado',max_length=12, choices=ESTADO_CREAR_CLINICA, default=SOLICITADO)
    solal_estado_msg = models.CharField('mensaje sobre el estado', max_length= 512)
    solal_token_confirmar_mail = models.CharField('token para confirmar mail', max_length= 128,null='true', blank='true')
    creado = models.DateTimeField(auto_now_add=True, blank= True)

    def save(self, *args, **kwargs):        
        if not self.pk: #si no tiene pk, es insert

            #no pueden existir dos usuarios con el mismo nombre de usuario.
            if User.objects.filter(username = self.solal_usuario).exists():
                raise ValidationError('El usuario ya existe, Intente con otro nombre de usuario')

            #no pueden existir dos clínicas con el mismo nombre.
            if VetClinica.objects.filter(nombre = self.solal_nombre_clinica).exists():
                raise ValidationError('La clínica ya existe. Intente con otro nombre de clínica')

            #no puede existir dos Personal de clínica con el mismo email
            if VetPersonal.objects.filter(email = self.solal_email).exists():
                if self.solal_email != '<redigi>[una cuenta para pruebas]@gmail.com@gmail.com':
                    raise ValidationError('La dirección de email pertenece a otro usuario. Intente con otra dirección de email')

        super(SolicitarAltaClinica, self).save(*args, **kwargs)

    #solicitado > clinica creada > mail enviado > mail confirmado
    #solicitado > error al crear clínica
    #solicitado > vencido (si pasaron un par de días)
    #clinica creada > error al enviar mail
    #incluir una alerta al acceder sobre la importancia del mail confirmado

    class EventoProcesar (models.Model):
        def save(self, *args, **kwargs):
    #        if not self.pk: #si no tiene pk, es insert
    #            #registro tarea de envío de mails
    #            solicitar_clinica_enviar_mails()


            super(EventoProcesar, self).save(*args, **kwargs)