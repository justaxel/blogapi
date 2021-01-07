from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType,
    ObjectType
)

#from .resolvers.crud import get_one_author
#from .resolvers.query import get_one_author

gql_dir_path = 'src/gql/'
type_defs = load_schema_from_path(f'{gql_dir_path}schema.graphql')

query = QueryType()
author = ObjectType('Author')


schema = make_executable_schema(type_defs, query, author)