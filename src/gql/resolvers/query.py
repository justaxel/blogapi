import typing
from sqlalchemy import Column, and_

from ...database.models import tbl_account_author
from ...database.crud import AccountDB
from ...classes.accounts import Author
from ...utils.helper_funcs import dict_keys_to_camel_case, get_query_fields


async def resolve_query_get_single_author(_, info, username: str = None, email: str = None) -> typing.Optional[typing.Mapping]:

    request = await info.context['request'].json()
    gql_request = request['query']
    # get query fields from the raw graphql request
    query_fields = get_query_fields(gql_request)

    _db = AccountDB('author')
    cols = [Column(field) for field in query_fields]
    table = _db.table
    if username:
        where_clause = and_(table.c.username == username, table.c.account_status == 'active')
    elif email:
        where_clause = and_(table.c.email == email, table.c.account_status == 'active')
    author = await _db.fetch_one(cols, where_clause)
    if author:
        _author = dict_keys_to_camel_case(author)
        return _author
    else:
        return author

async def resolve_query_get_all_authors(_, info, **__):

    request = await info.context['request'].json()
    gql_request = request['query']
    print(gql_request)
    # get query fields from the raw graphql request
    query_fields = get_query_fields(gql_request, 'getAllAuthors')
    print(query_fields)
    _db = AccountDB('author')
    cols = [Column(field) for field in query_fields]
    authors = await _db.fetch_all(cols)
    _authors = [dict_keys_to_camel_case(dict(author)) for author in authors]
    return _authors
