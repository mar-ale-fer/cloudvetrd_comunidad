import graphene
import graphql_jwt

import hiscliapp.schema
import hiscliapp.schema_relay
import hiscliapp.schema_relay_raza
import hiscliapp.schema_django_raza
import hiscliapp.schema_django_duenio
import hiscliapp.schema_relay_clinica
import users.schema

class Query(
    users.schema.Query,
    #hiscliapp.schema.Query,
    hiscliapp.schema_django_raza.Query,
    hiscliapp.schema_django_duenio.Query,
    hiscliapp.schema_relay.RelayQuery,
    hiscliapp.schema_relay_raza.RelayQuery,
    hiscliapp.schema_relay_clinica.RelayQuery,
    graphene.ObjectType
):
    pass

class Mutation(
    users.schema.Mutation,
    #hiscliapp.schema.Mutation,
    hiscliapp.schema_relay.RelayMutation,
    hiscliapp.schema_relay_raza.RelayMutation,
    hiscliapp.schema_relay_clinica.RelayMutation,
    graphene.ObjectType
):
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    verify_token = graphql_jwt.Verify.Field()
    refresh_token = graphql_jwt.Refresh.Field()
    #pass

schema = graphene.Schema(query=Query, mutation=Mutation)
