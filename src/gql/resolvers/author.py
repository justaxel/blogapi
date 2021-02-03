from ariadne import ObjectType
import sqlalchemy
from ...database.crud import AccountProfileInformationDB, StoryDB
from .query_helpers import get_gql_query, add_table_prefix_to_gql_query_items
from .utils import remove_table_prefix_from_dict, dict_keys_to_camel_case

author = ObjectType('Author')


@author.field('profileInfo')
async def resolve_profile_info(obj, info, *_):

    # get query fields from the raw graphql request and curate it
    request = await info.context['request'].json()
    gql_request = request['query']
    query_fields = get_gql_query(gql_request, has_args=True, only_main_query=False, only_subquery=True)
    _db = AccountProfileInformationDB()
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    author_id = obj['id']
    if author_id:
        where_clause = _db.table.c.author_id_fk == author_id
        profile_info = await _db.fetch_one(cols, where_clause)
        if profile_info:
            _profile_info = remove_table_prefix_from_dict(profile_info, tbl_prefix)
            author_profile_info = dict_keys_to_camel_case(_profile_info)
            return author_profile_info
    else:
        return None


@author.field('stories')
async def resolve_stories(obj, info, *_):

    request = await info.context['request'].json()
    gql_request = request['query']
    query_fields = get_gql_query(gql_request, has_args=True, only_main_query=False, only_subquery=True)
    _db = StoryDB()
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    author_id = obj['id']