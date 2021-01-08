from ...database.models import tbl_author
from ...database.crud import get_one_author


async def resolve_author(*_, username: str = None, email: str = None):
    if username:
        where_vals = {'username': username}
        cols = [tbl_author.c.id, tbl_author.c.username, tbl_author.c.email, tbl_author.c.account_status]
        author = await get_one_author(cols, where_vals)
        if author:
            return dict(author)
        else:
            return None

    elif email:
        where_vals = {'email': email}
        cols = [tbl_author.c.id, tbl_author.c.username, tbl_author.c.email, tbl_author.c.account_status]
        author = await get_one_author(cols, where_vals)
        if author:
            return dict(author)
        else:
            return None
    else:
        return 'Please enter either the Author\'s username or email'

