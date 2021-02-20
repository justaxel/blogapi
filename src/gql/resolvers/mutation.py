from sqlalchemy import or_

from ...accounts.accounts import Artist
from ...database.verification import AccountDataVerification


async def resolve_new_artist(
        *_,
        username: str = None,
        email: str = None,
        password: str = None,
        passwordConfirm: str = None
) -> dict:

    dirty_data = {
            'username': username,
            'email': email,
            'password': password,
            'password_confirm': passwordConfirm
        }
    verify_data = AccountDataVerification(dirty_data)
    if verify_data.is_data_valid():
            
        artist = Artist(username, email, password)
        table = artist.db.table
        where_clause = or_(table.c.username == username, table.c.email == email)
        existing_artist = await artist.db.fetch_one([table.c.id], where_clause)

        if not existing_artist:
            # ! Set this to not active when ready to verify email.
            artist.set_status('active')
            artist.hash_password()
            # get new artist's data dictionary
            new_artist_data = artist.spew_out_data()
            transaction = artist.db.transaction()
            try:
                await transaction.start()
                result = await artist.db.create_account(new_artist_data)
            except Exception:
                await transaction.rollback()
            else:
                if result:
                    await transaction.commit()
                    return {'status': True, 'artistID': result}
                else:
                    return {'status': False, 'error': 'Oops! Something happened.'}
        else:
            return {'status': False, 'error': 'An artist with those credentials already exist.'}
    return {'status': False, 'error': 'Data is not valid.'}
