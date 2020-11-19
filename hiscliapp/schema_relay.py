import graphene
import django_filters
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import VetMascota


class VetMascotaFilter(django_filters.FilterSet):
    class Meta:
        model = VetMascota
        fields = [
            'codigo', 'nombre',
            'especie', 'color', 'sexo'
        ]

class VetMascotaNode(DjangoObjectType):
    class Meta:
        model = VetMascota
        interfaces = (graphene.relay.Node,)

class RelayQuery(graphene.ObjectType):
    relay_mascota = graphene.relay.Node.Field(VetMascotaNode)
    relay_mascotas = DjangoFilterConnectionField(VetMascotaNode, filterset_class=VetMascotaFilter)

class RelayCreateVetMascota(graphene.relay.ClientIDMutation):
    mascota = graphene.Field(VetMascotaNode)

    class Input:
        codigo = graphene.String()
        nombre = graphene.String()
        fechaNacimiento = graphene.types.datetime.Date()
        especie = graphene.String()
        color = graphene.String()
        sexo = graphene.String()
        ultimaConsulta = graphene.types.datetime.Date()

    def mutate_and_get_payload(root, info, **input):
        #user = info.context.user or None
        mascota = VetMascota(
            codigo = input.get('codigo'),
            nombre = input.get('nombre'),
            fecha_nacimiento = input.get('fechaNacimiento'),
            especie = input.get('especie'),
            color = input.get('color'),
            sexo = input.get('sexo'),
            ultima_consulta = input.get('ultimaConsulta'),
            #posted_by=user,
        )
        mascota.save()

        return RelayCreateVetMascota(mascota=mascota)

class RelayMutation(graphene.ObjectType):
    relay_create_mascota= RelayCreateVetMascota.Field()
