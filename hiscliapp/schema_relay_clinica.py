import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import VetClinica, VetPersonal


class VetClinicaFilter(django_filters.FilterSet):
    class Meta:
        model = VetClinica
        fields = [
            'nombre',
        ]

class VetClinicaNode(DjangoObjectType):
    class Meta:
        model = VetClinica
        interfaces = (graphene.relay.Node,)

class VetPersonalNode(DjangoObjectType):
    class Meta:
        model = VetPersonal
        interfaces = (graphene.relay.Node,)

class RelayQuery(graphene.ObjectType):
    relay_clinica = graphene.relay.Node.Field(VetClinicaNode)
    relay_clinicas = DjangoFilterConnectionField(VetClinicaNode, filterset_class=VetClinicaFilter)

class RelayCreateVetClinica(graphene.relay.ClientIDMutation):
    clinica = graphene.Field(VetClinicaNode)

    class Input:
        nombre = graphene.String()

    def mutate_and_get_payload(root, info, **input):
        #user = info.context.user or None
        clinica = VetClinica(
            nombre = input.get('nombre'),
            #posted_by=user,
        )
        clinica.save()

        return RelayCreateVetClinica(clinica=clinica)


class RelayMutation(graphene.ObjectType):
    relay_create_clinica= RelayCreateVetClinica.Field()
