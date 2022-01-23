from graphene_django import DjangoObjectType
from AouthIO.models import ClientUser as clu
import graphene

class ClientUser(DjangoObjectType):
    class Meta:
        model = clu

class Query(graphene.ObjectType):
    users = graphene.List(ClientUser)

    def resolve_users(self, info):
        return clu.objects.all()

schema = graphene.Schema(query=Query)