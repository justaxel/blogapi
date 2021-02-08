from ariadne import ObjectType
import sqlalchemy

from ...database.crud import AuthorDB
from .query_helpers import (
    get_graphql_request,
    get_graphql_query_attribs,
    remove_prefix_from_single_db_data,
    remove_prefix_from_multiple_db_data,
    add_table_prefix_to_gql_query_items,
)
from ..resolvers.utils import dict_keys_to_camel_case


story = ObjectType('Story')


@story.field('authors')
async def resolve_authors(obj, info, *_):

    gql_request = await get_graphql_request(info)
    query_fields = get_graphql_query_attribs(
        gql_request, has_args=True, only_main_attribs=False, only_subquery_attribs=True, subquery_name='authors'
    )
    _db = AuthorDB()
    tbl_prefix = _db.attrib_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    story_id = obj['id']
    where_clause = {'story_id': story_id}
    story_author = await _db.fetch_story_authors(cols, where_clause)
    _author = remove_prefix_from_multiple_db_data(story_author, tbl_prefix)
    authors = [dict_keys_to_camel_case(author) for author in _author]
    return authors
