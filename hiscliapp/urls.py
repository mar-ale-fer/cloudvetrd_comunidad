 # -- coding: utf-8 --
from django.urls import path
from django.conf.urls import url, include

from django.urls import reverse_lazy

from django.conf import settings
from django.conf.urls.static import static
from .viewlogin import user_login, user_logout
#veterinaria
from .viewvetduenio import VetDuenioCrear, VetDuenioBorrar, VetDuenioDetalle, VetDuenioListar, VetDuenioModificar
#mascotas del dueño:
from .viewvetduenio import VetDuenioMascotasDetalle

from .view_duenio_mascota import admin_vetmascota
from .view_vetmascota_vetconsulta import admin_vetconsulta
from .viewvetraza import VetRazaCrear, VetRazaBorrar, VetRazaDetalle, VetRazaListar, VetRazaModificar
from .viewvetmascota import VetMascotaListar, VetMascotaCrear, VetMascotaModificar, VetMascotaBorrar, VetMascotaDetalle
from .viewvetconsulta import VetConsultaCrear, VetConsultaModificar, VetConsultaBorrar
from .view_ajax_localidades import ajax_lista_paises, ajax_lista_provincias, ajax_lista_localidades
from .viewlocalidad_prompt import LocalidadPrompt
#autogestion. alta de clínica
from .viewsolal import SolicitarAltaClinicaCrear
#autogestion. confirmar direcciòn de mail
from .view_usuario_confirmar_mail import usuario_confirmar_mail

from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views#registración

from .view_crear_clinica import crear_clinica

app_name="hiscliapp" #namespace


urlpatterns = [
    #Registración
    #https://simpleisbetterthancomplex.com/tutorial/2016/09/19/how-to-create-password-reset-view.html
    #url('^', include('django.contrib.auth.urls')),  
    #url(r'^', include('django.contrib.auth.urls')),
    #path('password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    #path('password-reset/<uidb64>/<token>/', empty_view, name='password_reset_confirm'),
    #url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'), 

    #resuelto:
    #https://stackoverflow.com/questions/47033030/reverse-for-password-reset-done-not-found-password-reset-done-is-not-a-vali
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url = reverse_lazy('hiscliapp:password_reset_done')
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url = reverse_lazy('hiscliapp:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password_reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    #autogestion. alta de clínica
    path('altaclinica/', SolicitarAltaClinicaCrear.as_view(), name='ag_alta_clinica'),
    path('crear_clinica/', crear_clinica, name='ag_crear_clinica'),

    #confirmar mail del usuario
    path('usuario_confirmar_mail/<str:cloudvet_token>/', usuario_confirmar_mail, name='usuario_confirmar_mail'),

    #Login y logout
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),    
    #veterinaria
    #dueño
    url(r'^vetduenio/$', login_required(VetDuenioListar.as_view()), name='vetduenio_listar'),
    url(r'^vetduenio/crear/$', login_required(VetDuenioCrear.as_view()), name='vetduenio_crear'),
    url(r'^vetduenio/(?P<pk>\d+)/$', login_required(VetDuenioDetalle.as_view()), name='vetduenio_detalle'),
    #nuevo diseño plano
    url(r'^vetduenio/mascotas/(?P<pk>\d+)/$', login_required(VetDuenioMascotasDetalle.as_view()), name='vetduenio_mascotas'),

    url(r'^vetduenio/(?P<pk>\d+)/modificar/$', login_required(VetDuenioModificar.as_view()), name='vetduenio_modificar'),
    url(r'^vetduenio/(?P<pk>\d+)/borrar/$', login_required(VetDuenioBorrar.as_view()), name='vetduenio_borrar'), 
    url(r'^vetduenio/(?P<pk>\d+)/vetmascota$', login_required(admin_vetmascota.as_view()), name='vetduenio_vetmascota'), 
    url(r'^vetmascota/(?P<pk>\d+)/vetconsulta$', login_required(admin_vetconsulta.as_view()), name='vetmascota_vetconsulta'), 
    #raza
    path('vetraza/', VetRazaListar.as_view(), name='vetraza_listar'),
    path('vetraza/crear/', login_required(VetRazaCrear.as_view()), name='vetraza_crear'),
    path('vetraza/<int:pk>/', login_required(VetRazaDetalle.as_view()), name='vetraza_detalle'),
    path('vetraza/<int:pk>/modificar/', login_required(VetRazaModificar.as_view()), name='vetraza_modificar'),
    path('vetraza/<int:pk>/borrar/', login_required(VetRazaBorrar.as_view()), name='vetraza_borrar'), 
    #mascota
    path('vetmascota/', login_required(VetMascotaListar.as_view()), name='vetmascota_listar'),
    path('vetmascota/crear/duenio/<int:vetduenio_id>/', login_required(VetMascotaCrear.as_view()), name='vetmascota_crear'),
    path('vetmascota/<int:pk>/modificar/', login_required(VetMascotaModificar.as_view()), name='vetmascota_modificar'),
    path('vetmascota/<int:pk>/borrar/', login_required(VetMascotaBorrar.as_view()), name='vetmascota_borrar'),
    path('vetmascota/<int:pk>/', login_required(VetMascotaDetalle.as_view()), name='vetmascota_detalle'),
    #consulta
    path('vetconsulta/crear/mascota/<int:vetmascota_id>/', login_required(VetConsultaCrear.as_view()), name='vetconsulta_crear'),
    path('vetconsulta/<int:pk>/modificar/', login_required(VetConsultaModificar.as_view()), name='vetconsulta_modificar'),
    path('vetconsulta/<int:pk>/borrar/', login_required(VetConsultaBorrar.as_view()), name='vetconsulta_borrar'),


    #ajax localidades
    url(r'^ajax/paises/$', login_required(ajax_lista_paises), name= 'ajax_paises'),
    url(r'^ajax/(?P<id_pais>\d+)/provincias/$', login_required(ajax_lista_provincias), name= 'ajax_provincias'),
    url(r'^ajax/(?P<id_provincia>\d+)/localidades/$', login_required(ajax_lista_localidades), name= 'ajax_localidades'),
    url(r'^localidadprompt/$', LocalidadPrompt.as_view(), name='localidad_prompt'),    

] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)



