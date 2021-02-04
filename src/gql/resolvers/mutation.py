from typing import Optional
from sqlalchemy import or_
from ...database.main import DB

from ...accounts.accounts import Author
from ...database.crud import AccountDB
from ...database.verification import AccountDataVerification


async def resolve_new_author(*_, username: str = None, email: str = None, password: str = None, passwordConfirm: str = None) -> dict:

    dirty_data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': passwordConfirm
        }
    verify_data = AccountDataVerification(dirty_data)
    if verify_data.is_data_valid():
            
        author = Author(username, email, password)
        table = author._db.table
        where_clause = or_(table.c.username == username, table.c.email == email)
        existing_author = await author._db.fetch_one([table.c.id], where_clause)

        if not existing_author:
            # ! Set this to not active when ready to verify email.
            author.set_status('active')
            author.hash_password()
            # get new author's data dictionary
            new_author_data = author.spew_out_data()
            transaction = DB.transaction()
            try:
                await transaction.start()
                result = await author._db.create_account(new_author_data)
            except Exception:
                await transaction.rollback()
            else:
                if result:
                    await transaction.commit()
                    return {'status': True, 'authorID': result}
                else:
                    {'status': False, 'error': 'Oops! Something happened.'}
        else:
            return {'status': False, 'error': 'An author with those credentials already exist.'}
    return {'status': False, 'error': 'Data is not valid.'}
