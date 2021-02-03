from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    ObjectType,
    MutationType
)

from .resolvers.author import author
from .resolvers.query import query

#from .resolvers.query import (
#    resolve_query_get_single_author,
#    resolve_query_get_all_authors,
#    resolve_query_get_story,
#    resolve_query_get_all_stories_by_author
#)
from .resolvers.mutation import (
    resolve_new_author,
)


gql_path = 'src/gql/'
type_defs = load_schema_from_path(f'{gql_path}schema.graphql')

mutation = MutationType()


story = ObjectType('Story')
author_profile = ObjectType('AuthorProfile')


new_author_payload = ObjectType('NewAuthorPayload')
new_story_payload = ObjectType('NewStoryPayload')

mutation.set_field('newAuthor', resolve_new_author)

schema = make_executable_schema(
    type_defs,
    query, mutation, author, story 
)