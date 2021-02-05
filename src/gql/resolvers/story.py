from ariadne import ObjectType
import sqlalchemy

from ...database.crud import AccountDB
from .query_helpers import (
    get_graphql_request,
    get_graphql_query_attribs,
    remove_prefix_from_single_db_data,
    add_table_prefix_to_gql_query_items
)

story = ObjectType('Story')


@story.field('authors')
async def resolve_authors(obj, info, *_):

    gql_request = await get_graphql_request(info)
    query_fields = get_graphql_query_attribs(
        gql_request, has_args=True, only_main_attribs=False, only_subquery_attribs=True, subquery_name='authors'
    )
    _db = AccountDB('author')
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
