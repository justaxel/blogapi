from ariadne import ObjectType
import sqlalchemy

from ...database.crud import AccountProfileInformationDB, StoryDB
from .query_helpers import (
    get_graphql_query_attribs,
    add_table_prefix_to_gql_query_items,
    remove_prefix_from_single_db_data,
    remove_prefix_from_multiple_db_data,
    get_graphql_request
)
from .utils import dict_keys_to_camel_case


author = ObjectType('Author')


@author.field('profileInfo')
async def resolve_profile_info(obj, info, *_):

    # get query fields from the raw graphql request and curate it
    gql_request = await get_graphql_request(info)
    query_fields = get_graphql_query_attribs(
        gql_request, has_args=True, only_main_attribs=False, only_subquery_attribs=True, subquery_name='profile_info'
    )
    _db = AccountProfileInformationDB()
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    author_id = obj['id']
    if author_id:
        where_clause = sqlalchemy.and_(_db.table.c.author_id_fk == author_id)
        profile_info = await _db.fetch_one(cols, where_clause)
        if profile_info:
            _profile_info = remove_prefix_from_single_db_data(profile_info, tbl_prefix)
            author_profile_info = dict_keys_to_camel_case(_profile_info)
            return author_profile_info
    else:
        return None


@author.field('stories')
async def resolve_stories(obj, info, *_):

    gql_request = await get_graphql_request(info)
    query_fields = get_graphql_query_attribs(
        gql_request, has_args=True, only_main_attribs=False, only_subquery_attribs=True, subquery_name='stories'
    )
    _db = StoryDB()
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    author_id = obj['id']
    where_clause = {'author_id': author_id}
    author_stories = await _db.fetch_author_stories(cols, where_clause)
    _stories = remove_prefix_from_multiple_db_data(author_stories, tbl_prefix)
    stories = [dict_keys_to_camel_case(story) for story in _stories]
    return stories
