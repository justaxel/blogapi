from ariadne import (
    load_schema_from_path,
    make_executable_schema,
    ObjectType,
    MutationType
)

from .resolvers.query import query
from .resolvers.mutation import (
    resolve_new_artist,
)
from .resolvers.artist import artist
from .resolvers.story import story


gql_path = 'src/gql/'
type_defs = load_schema_from_path(f'{gql_path}schema.graphql')

mutation = MutationType()


artist_profile = ObjectType('ArtistProfile')


new_artist_payload = ObjectType('NewArtistPayload')
new_story_payload = ObjectType('NewStoryPayload')

mutation.set_field('newArtist', resolve_new_artist)

schema = make_executable_schema(
    type_defs,
    query, mutation, artist, story
)
