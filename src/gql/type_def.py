from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    QueryType,
    ObjectType,
    MutationType
)

from .resolvers.query import (
    resolve_query_get_single_author,
    resolve_query_get_all_authors
)
from .resolvers.mutation import (
    resolve_new_author,
)


gql_path = 'src/gql/'
type_defs = load_schema_from_path(f'{gql_path}schema.graphql')

query = QueryType()
mutation = MutationType()


author = ObjectType('Author')

new_author_payload = ObjectType('NewAuthorPayload')
new_story_payload = ObjectType('NewStoryPayload')

query.set_field('getOneAuthor', resolve_query_get_single_author)
query.set_field('getAllAuthors', resolve_query_get_all_authors)

mutation.set_field('newAuthor', resolve_new_author)

schema = make_executable_schema(type_defs, query, author, mutation)