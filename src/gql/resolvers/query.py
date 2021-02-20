"""

"""


import typing
from uuid import UUID
import sqlalchemy
from ariadne import QueryType
from graphql.type.definition import GraphQLResolveInfo

from ...database.crud import ArtistDB, StoryDB
from .query_processor import get_graphql_request, GraphQLQueryProcessor

from .utils import (
    from_snake_dict_keys_to_camel_case_keys,
    add_db_table_prefix_to_gql_query_fields,
    remove_db_table_prefix_from_retrieved_db_data
)


query = QueryType()


@query.field('getArtist')
async def resolve_get_artist(
        _,
        info: GraphQLResolveInfo,
        username: str = None,
        email: str = None
) -> typing.Optional[typing.Mapping]:
    """

    Args:
        _:
        info:
        username:
        email:

    Returns:

    """

    # get gql request query, process it and obtain the fields
    gql_request_query = await get_graphql_request(info)
    gql_query_processor = GraphQLQueryProcessor(gql_request_query, query_has_args=True)
    global_query_fields = gql_query_processor.retrieve_query_fields()
    root_q_fields = global_query_fields.pop('root_query_fields')
    # add subqueries to gql context dictionary so they can pass through
    info.context.update(global_query_fields)

    _db = ArtistDB()
    tbl_prefix = _db.attrib_prefix

    # prepend the corresponding tbl prefix to every query field requested
    # and turn it into an appropriate sqlalchemy column
    query_fields = add_db_table_prefix_to_gql_query_fields(root_q_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in query_fields]
    where_clause = sqlalchemy.and_()
    if username:
        where_clause = sqlalchemy.and_(
            _db.table.c.account_artist_username == username, _db.table.c.account_author_status == 'active'
        )
    elif email:
        where_clause = sqlalchemy.and_(
            _db.table.c.account_artist_email == email, _db.table.c.account_author_status == 'active'
        )

    artist = await _db.fetch_one(cols, where_clause)
    if artist:
        _artist = remove_db_table_prefix_from_retrieved_db_data(author, tbl_prefix)
        artist = from_snake_dict_keys_to_camel_case_keys(_author)
    return artist


@query.field('getStory')
async def resolve_get_story(
        _,
        info: GraphQLResolveInfo,
        _id: UUID = None,
        title: str = None
) -> typing.Optional[typing.Mapping]:
    """

    Args:
        _:
        info:
        _id:
        title:

    Returns:

    """

    # get query fields from the raw graphql request and curate it
    gql_request_query = await get_graphql_request(info)
    gql_query_processor = GraphQLQueryProcessor(gql_request_query, query_has_args=True)
    global_query_fields = gql_query_processor.retrieve_query_fields()
    root_q_fields = global_query_fields.pop('root_query_fields')
    info.context.update(global_query_fields)

    _db = StoryDB()
    query_fields = add_db_table_prefix_to_gql_query_fields(root_q_fields, _db.attribute_prefix)
    cols = [sqlalchemy.Column(field) for field in query_fields]

    where_clause = sqlalchemy.and_()
    if _id:
        where_clause = sqlalchemy.and_(_db.table.c.story_id == _id)
    elif title:
        where_clause = sqlalchemy.and_(_db.table.c.story_title == title)

    story = await _db.fetch_one(cols, where_clause)
    _story = remove_db_table_prefix_from_retrieved_db_data(story, _db.attribute_prefix)
    story = from_snake_dict_keys_to_camel_case_keys(_story)
    return story


@query.field('getAllArtists')
async def resolve_get_all_artists(_, info: GraphQLResolveInfo) -> typing.Optional[typing.Mapping]:
    """

    Args:
        _:
        info:

    Returns:

    """

    gql_request_query = await get_graphql_request(info)
    gql_request_processor = GraphQLQueryProcessor(gql_request_query)
    global_query_fields = gql_request_processor.retrieve_query_fields()
    root_q_fields = global_query_fields.pop('root_query_fields')
    info.context.update(global_query_fields)

    _db = ArtistDB()
    tbl_prefix = _db.attrib_prefix

    query_fields = add_db_table_prefix_to_gql_query_fields(root_q_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in query_fields]
    artists = await _db.fetch_all(cols)
    _artists = remove_db_table_prefix_from_retrieved_db_data(artists, tbl_prefix)
    artists = [from_snake_dict_keys_to_camel_case_keys(author) for author in _artists]
    return artists


@query.field('getAllStoriesByArtist')
async def resolve_get_all_stories_by_artist(
        _,
        info: GraphQLResolveInfo,
        _id: None
) -> typing.Optional[typing.Mapping]:
    """

    Args:
        _:
        info:
        _id:

    Returns:

    """

    gql_request_query = await get_graphql_request(info)
    gql_query_processor = GraphQLQueryProcessor(gql_request_query)
    global_query_fields = gql_query_processor.retrieve_query_fields()
    root_query_fields = global_query_fields.pop('root_query_fields')
    info.context.update(global_query_fields)

    _db = StoryDB()
    tbl_prefix = _db.attribute_prefix

    query_fields = add_db_table_prefix_to_gql_query_fields(root_query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in query_fields]
    where_clause_val = {'artist_id': _id}
    stories = await _db.fetch_artist_stories(cols, where_clause_val)
    _stories = remove_db_table_prefix_from_retrieved_db_data(stories, tbl_prefix)
    stories = [from_snake_dict_keys_to_camel_case_keys(story) for story in _stories]
    return stories
