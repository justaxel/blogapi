from ...database.models import tbl_author
from ...database.crud import get_one_author, get_all_authors
from ...utils.helper_funcs import to_camel_case


# resolver function for single author query
async def resolve_author(info, *_, username: str = None, email: str = None):
    print(await info.context['request'].json())
    if username:
        where_vals = {'username': username}
        cols = [
            tbl_author.c.id, tbl_author.c.username, tbl_author.c.email, 
            tbl_author.c.account_status, tbl_author.c.date_created
        ]
        author = await get_one_author(cols, where_vals)
        if author:
            _author = dict(author)
            for key in _author.keys():
                to_camel_case(key)
            print(_author)
            return _author
        else:
            return None

    elif email:
        where_vals = {'email': email}
        cols = [
            tbl_author.c.id, tbl_author.c.username, tbl_author.c.email,
            tbl_author.c.account_status, tbl_author.c.date_created
        ]
        author = await get_one_author(cols, where_vals)
        if author:
            _author = dict(author)
            for key in _author.keys():
                to_camel_case(key)
            print(_author)
            return _author
        else:
            return None


# resolver function for all authors query
async def resolve_authors(*_, **__):
    authors = await get_all_authors()
    _authors = [dict(author) for author in authors]
    print(_authors)
    return _authors
