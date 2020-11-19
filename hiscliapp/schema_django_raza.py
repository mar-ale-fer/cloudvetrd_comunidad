import graphene
from graphene_django import DjangoObjectType
from django.db.models import Q
from .models import VetRaza

#def auth_required(queryset, args, request, info):
#  if request.user.is_authenticated():
#    return queryset
#
#  return queryset.none()

class VetRazaType(DjangoObjectType):
    class Meta:
        model = VetRaza

class Query(graphene.ObjectType):
    razas = graphene.List(VetRazaType,
    filtro_nombre= graphene.String(),
    first= graphene.Int(),
    skip=graphene.Int(),
)

    def resolve_razas(self, info,
       filtro_nombre=None,
       first=None,
       skip=None,
       **kwargs
    ):

        user = info.context.user
        if user.is_anonymous:
            raise Exception('No estás logueado!')

        qs = VetRaza.objects.all()
        if filtro_nombre:
            filter = (
            Q(nombre__unaccent__icontains=filtro_nombre)
            )
            qs= qs.filter(filter)

        if skip:
            qs= qs[skip::]

        if first:
            qs= qs[:first]

        return qs
