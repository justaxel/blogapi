import typing
import sqlalchemy
from ariadne import QueryType
from ...database.crud import AccountDB
from .query_helpers import (
    get_gql_query,
    add_table_prefix_to_gql_query_items
)
from .utils import remove_table_prefix_from_dict, dict_keys_to_camel_case

query = QueryType()


@query.field('getAuthor')
async def resolve_get_author(
        _,
        info,
        username: typing.Optional[str] = None,
        email: typing.Optional[str] = None
) -> typing.Optional[typing.Mapping[str, str]]:

    # get query fields from the raw graphql request and curate it
    request = await info.context['request'].json()
    gql_request = request['query']
    print(request)
    query_fields = get_gql_query(gql_request, has_args=True)

    _db = AccountDB('author')
    # get main query db table prefix and add it to every main query field requested
    tbl_prefix = _db.attribute_prefix
    q_fields_with_prefix = add_table_prefix_to_gql_query_items(query_fields, tbl_prefix)

    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
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
        _author = remove_table_prefix_from_dict(author, tbl_prefix)
        author = dict_keys_to_camel_case(_author)
    return author
