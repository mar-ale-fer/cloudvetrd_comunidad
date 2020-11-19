import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import VetRaza

def auth_required(queryset, args, request, info):
  if request.user.is_authenticated():
    return queryset

  return queryset.none()

class VetRazaFilter(django_filters.FilterSet):
    class Meta:
        model = VetRaza
        fields = [
            'nombre',
        ]

class VetRazaNode(DjangoObjectType):
    class Meta:
        model = VetRaza
        interfaces = (graphene.relay.Node,)
        #permissions = [auth_required]
# https://github.com/graphql-python/graphene-django/issues/79

class RelayQuery(graphene.ObjectType):
    relay_raza = graphene.relay.Node.Field(VetRazaNode)
    relay_razas = DjangoFilterConnectionField(VetRazaNode, filterset_class=VetRazaFilter)

class RelayCreateVetRaza(graphene.relay.ClientIDMutation):
    raza = graphene.Field(VetRazaNode)

    class Input:
        nombre = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        #user = info.context.user or None
        raza = VetRaza(
            nombre = input.get('nombre'),
            #posted_by=user,
        )
        raza.save()

        return RelayCreateVetRaza(raza=raza)

class RelayMutation(graphene.ObjectType):
    relay_create_raza= RelayCreateVetRaza.Field()
