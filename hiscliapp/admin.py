# -- coding: utf-8 --
from django.contrib import admin
 
from .models import Pais
from .models import Provincia
from .models import Localidad
from .models import TipoDocumento
from .models import Persona
#veterinaria
from .models import VetDuenio
from .models import VetMascota
from .models import VetMotivoConsulta
from .models import VetConsulta
from .models import VetConsultaImagen
from .models import VetRaza
from .models import VetClinica
from .models import VetPersonal
from .models import SolicitarAltaClinica
from .models import Numerador

admin.site.register(VetMotivoConsulta)
admin.site.register(VetConsulta)
admin.site.register(VetRaza)
admin.site.register(VetMascota)
admin.site.register(Numerador)

#+Clinica, su personal y razas
class VetPersonalInLine(admin.TabularInline):
	model = VetPersonal
	extra = 3

#+Clinica y su personal
class VetRazaInLine(admin.TabularInline):
	model = VetRaza
	extra = 1

class VetClinicaAdmin(admin.ModelAdmin):
    inlines = [VetPersonalInLine, VetRazaInLine]
    
    list_display = ('id','nombre','modo_pago','fecha_inicio','fecha_fin_free')

admin.site.register(VetClinica, VetClinicaAdmin)    
#-Clinica y su personal

#+Dueño y sus mascotas
class VetMascotaInline(admin.TabularInline):
    model = VetMascota
    extra = 1

class VetDuenioAdmin(admin.ModelAdmin):
    inlines = [VetMascotaInline]
    list_filter = ('apellido',)
    list_display = ('id','apellido','nombres','codigo','creado_por',)
    #def get_localidadnombre(self, obj):
    #    return obj.localidad.nombre
    #get_localidadnombre.admin_order_field  = 'localidad'  #Allows column order sorting
    #get_localidadnombre.short_description = 'nombre de la localidad'  #Renames column head   

admin.site.register(VetDuenio, VetDuenioAdmin)    
#-Dueño y sus mascotas

class VetPersonalAdmin(admin.ModelAdmin):
    list_display = ('id','usuario','clinica','email',)
    #def get_localidadnombre(self, obj):
    #    return obj.localidad.nombre
    #get_localidadnombre.admin_order_field  = 'localidad'  #Allows column order sorting
    #get_localidadnombre.short_description = 'nombre de la localidad'  #Renames column head   

admin.site.register(VetPersonal, VetPersonalAdmin)    
#-Dueño y sus mascotas


#+solicitar alta clinica
class SolicitarAltaClinicaAdmin(admin.ModelAdmin):
    list_filter = ('solal_estado',)
    list_display = ('id',
    'solal_nombre_clinica',
    'solal_usuario',
    'solal_clave',
    'solal_apellido',
    'solal_nombre',
    'solal_email',
    'solal_celular',
    'solal_estado',
    'solal_estado_msg',
    'creado'
    ,)
    #def get_localidadnombre(self, obj):
    #    return obj.localidad.nombre
    #get_localidadnombre.admin_order_field  = 'localidad'  #Allows column order sorting
    #get_localidadnombre.short_description = 'nombre de la localidad'  #Renames column head   

admin.site.register(SolicitarAltaClinica, SolicitarAltaClinicaAdmin)    
#-solicitar alta clinica



admin.site.register(Pais)
admin.site.register(Persona)

class ProvinciaAdmin(admin.ModelAdmin):
    model = Provincia
    list_display = ('nombre','get_paisnombre',)

    def get_paisnombre(self, obj):
        return obj.pais.nombre
    get_paisnombre.admin_order_field  = 'pais'  #Allows column order sorting
    get_paisnombre.short_description = 'nombre del pais' #Renames column head

class LocalidadAdmin(admin.ModelAdmin):
    list_display = ('nombre','get_paisnombre')
    
    def get_paisnombre(self, obj):
        return obj.provincia.pais.nombre
    get_paisnombre.admin_order_field  = 'pais'  #Allows column order sorting
    get_paisnombre.short_description = 'nombre del pais'  #Renames column head    
    
class TipoDocumentoAdmin(admin.ModelAdmin):
    list_display = ('nombre','get_paisnombre',)

    def get_paisnombre(self, obj):
        return obj.pais.nombre
    get_paisnombre.admin_order_field  = 'pais'  #Allows column order sorting
    get_paisnombre.short_description = 'nombre del pais'  #Renames column head    

admin.site.register(Provincia, ProvinciaAdmin)
admin.site.register(Localidad, LocalidadAdmin)
admin.site.register(TipoDocumento, TipoDocumentoAdmin)



