from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType,
    ObjectType
)

#from .resolvers.crud import get_one_author
from .resolvers.query import resolve_author

gql_path = 'src/gql/'
type_defs = load_schema_from_path(f'{gql_path}schema.graphql')

query = QueryType()
author = ObjectType('Author')
user = ObjectType('User')

@query.field('user')
async def resolve_user(_, info):
    print('here is the resolve user(form query)')
    print(info)
    print('----')
    print(dict(info.context['request']))
    return info.context['request']

@user.field('username')
async def resolve_username(obj, info):
    print('Here is the resolve usernameinfo:')
    print(info)
    print('---')
    print(dict(obj))
    return 'hello'


query.set_field('author', resolve_author)
schema = make_executable_schema(type_defs, query, author, user)