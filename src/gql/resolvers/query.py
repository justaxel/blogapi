import typing
from uuid import UUID
import sqlalchemy
from ariadne import QueryType

from ...database.crud import AuthorDB, StoryDB
from .query_helpers import (
    get_graphql_query_attribs,
    add_table_prefix_to_gql_query_items,
    get_graphql_request,
    remove_prefix_from_single_db_data,
)
from .utils import dict_keys_to_camel_case


query = QueryType()


@query.field('getAuthor')
async def resolve_get_author(
        _,
        info,
        username: str = None,
        email: str = None
) -> typing.Optional[typing.Mapping]:

    # get query fields from the raw graphql request and curate it
    gql_request = await get_graphql_request(info)
    query_fields = get_graphql_query_attribs(gql_request, has_args=True)
    info.context['hello'] = 'im the root'

    _db = AuthorDB()
    # get main query db table prefix and add it to every main query field requested
    tbl_prefix = _db.attrib_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)

    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    where_clause = sqlalchemy.and_()
    if username:
        where_clause = sqlalchemy.and_(
            _db.table.c.account_author_username == username, _db.table.c.account_author_status == 'active'
        )
    elif email:
        where_clause = sqlalchemy.and_(
            _db.table.c.account_author_email == email, _db.table.c.account_author_status == 'active'
        )

    author = await _db.fetch_one(cols, where_clause)
    if author:
        _author = remove_prefix_from_single_db_data(author, tbl_prefix)
        author = dict_keys_to_camel_case(_author)
    return author


@query.field('getStory')
async def resolve_get_story(
        _,
        info,
        _id: UUID = None,
        title: str = None
) -> typing.Optional[typing.Mapping]:

    # get query fields from the raw graphql request and curate it
    request = await info.context['request'].json()
    print(request)
    gql_request = request['query']
    query_fields = get_graphql_query_attribs(gql_request, has_args=True, )
    _db = StoryDB()
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]

    where_clause = sqlalchemy.and_()
    if _id:
        where_clause = sqlalchemy.and_(_db.table.c.story_id == _id)
    elif title:
        where_clause = sqlalchemy.and_(_db.table.c.story_title == title)

    story = await _db.fetch_one(cols, where_clause)
    _story = remove_prefix_from_single_db_data(story, tbl_prefix)
    story = dict_keys_to_camel_case(_story)
    return story
