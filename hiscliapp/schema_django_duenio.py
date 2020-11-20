import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import VetDuenio, VetPersonal, TipoDocumento

#def auth_required(queryset, args, request, info):
#  if request.user.is_authenticated():
#    return queryset
#
#  return queryset.none()

class VetDuenioType(DjangoObjectType):
    class Meta:
        model = VetDuenio

class TipoDocumentoType(DjangoObjectType):
    class Meta:
        model = TipoDocumento

class Query(graphene.ObjectType):
    duenios = graphene.List(VetDuenioType,
    filtro_nombre= graphene.String(),
    first= graphene.Int(),
    skip=graphene.Int(),
)

    def resolve_duenios(self, info,
       filtro_nombre=None,
       first=None,
       skip=None,
       **kwargs
    ):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('No estás logueado!')

        if not user.is_active:
            raise Exception('Usuario inactivo!')

        personal_del_usuario = VetPersonal.objects.get( usuario = user) #busco al personal asociado al usuario
        clinica = personal_del_usuario.clinica
        id_clinica = str(clinica.id)
        clinica_nombre = clinica.nombre
        clinica_imagen = str(clinica.imagen)

        user.id_clinica = id_clinica

        qs = VetDuenio.objects.all()
        qs = qs.filter(clinica__id = id_clinica)
        if filtro_nombre:
            filter = (
            Q(nombres__unaccent__icontains=filtro_nombre)
            )
            qs= qs.filter(filter)

        if skip:
            qs= qs[skip::]

        if first:
            qs= qs[:first]

        return qs
