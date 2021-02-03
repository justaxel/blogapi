import typing
from sqlalchemy import Column, and_

from ...database.crud import AccountDB, StoryDB
from .query_helpers import get_gql_query, add_table_prefix_to_gql_query_items
from .utils import (
    remove_table_prefix_from_dict,
    dict_keys_to_camel_case,
)


async def resolve_query_get_single_author(_, info, username: str = None, email: str = None) -> typing.Optional[typing.Mapping]:

    request = await info.context['request'].json()
    gql_request = request['query']
    # get query fields from the raw graphql request
    query_fields = get_gql_query(gql_request, has_args=True)

    _db = AccountDB('author')
    table_prefix = _db.get_attrib_prefix()
    _query_fields = add_table_prefix_to_gql_query_items(query_fields, table_prefix)
    query_atrribs = _query_fields['main_query']
    cols = [Column(field) for field in query_atrribs]
    table = _db.table

    if username:
        where_clause = and_(
            table.c.account_author_username == username, table.c.account_author_status == 'active'
        )
    elif email:
        where_clause = and_(
            table.c.account_author_email == email, table.c.account_author_status == 'active'
        )

    author = await _db.fetch_one(cols, where_clause)
    if author:
        _author = remove_table_prefix_from_dict(author, table_prefix)
        author = dict_keys_to_camel_case(_author)
    return author


async def resolve_query_get_all_authors(_, info, **__) -> typing.Optional[typing.List[typing.Dict[str, str]]]:

    request = await info.context['request'].json()
    gql_request = request['query']
    # get query fields from the raw graphql request
    query_fields = get_gql_query(gql_request, query_name='getAllAuthors')

    _db = AccountDB('author')
    table_prefix = _db.get_attrib_prefix()
    _query_fields = add_table_prefix_to_gql_query_items(query_fields, table_prefix)
    query_attribs = _query_fields['main_query']
    cols = [Column(field) for field in query_attribs]

    authors = await _db.fetch_all(cols)
    if authors:
        _authors = [remove_table_prefix_from_dict(author, table_prefix) for author in authors]
        authors = [dict_keys_to_camel_case(author) for author in _authors]
    return authors


async def resolve_query_get_story(_, info, **__):
    pass


async def resolve_query_get_all_stories_by_author(_, info, username: str = None) -> typing.Optional[typing.List[typing.Dict[str, str]]]:
    
    request = await info.context['request'].json()
    gql_request = request['query']
    query_fields = get_gql_query(gql_request, has_args=True)
    _db = StoryDB()
    story_table_prefix = _db.get_attrib_prefix()
    author_table_prefix = AccountDB('author').get_attrib_prefix()
    subq_prefix = {'authors': author_table_prefix}
    _query_fields = add_table_prefix_to_gql_query_items(query_fields, story_table_prefix, subq_prefix)
    story_attribs = _query_fields['main_query']
    author_attribs = _query_fields['subqueries']['authors']
    story_cols = [Column(field) for field in story_attribs]
    author_cols = [Column(field) for field in author_attribs]
    cols = story_cols + author_cols
    where_clause = {'username': username}
    author_stories = await _db.fetch_author_stories(cols, where_clause)
    if author_stories:
        print([dict(story) for story in author_stories])
        return [dict(story) for story in author_stories] 