import graphene
from graphene_django import DjangoObjectType

from .models import VetMascota

class VetMascotaType(DjangoObjectType):
    class Meta:
        model = VetMascota
"""
class Query(graphene.ObjectType):
    mascotas = graphene.List(VetMascotaType)

    def resolve_mascotas(self, info, **kwargs):
        return VetMascota.objects.all()
"""
class CreateMascota(graphene.Mutation):
    codigo = graphene.Int()
    nombre = graphene.String()
    fechaNacimiento = graphene.types.datetime.Date()
    especie = graphene.String()
    color = graphene.String()
    sexo = graphene.String()
    ultimaConsulta = graphene.types.datetime.Date()

    class Arguments:
        codigo = graphene.String()
        nombre = graphene.String()
        fechaNacimiento = graphene.types.datetime.Date()
        especie = graphene.String()
        color = graphene.String()
        sexo = graphene.String()
        ultimaConsulta = graphene.types.datetime.Date()

    def mutate(self,info,codigo, nombre, fechaNacimiento, especie, color, sexo, ultimaConsulta ):
        #código python
        mascota = VetMascota(
            codigo = codigo,
            nombre = nombre,
            fecha_nacimiento = fechaNacimiento,
            especie = especie,
            color = color,
            sexo = sexo,
            ultima_consulta = ultimaConsulta
        )
        mascota.save()

        return CreateMascota(
            id = mascota.id,
            codigo = mascota.codigo,
            nombre = mascota.nombre,
            fechaNacimiento = mascota.fecha_nacimiento,
            especie = mascota.especie,
            color = mascota.color,
            sexo = mascota.sexo,
            ultimaConsulta = mascota.ultima_consulta
        )

class Mutation(graphene.ObjectType):
     create_mascota = CreateMascota.Field()
