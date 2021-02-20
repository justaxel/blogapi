"""

"""


from fastapi import FastAPI
from ariadne.asgi import GraphQL
from .gql.type_def import schema

from .settings import DB_NAME
from .database.main import MAIN_DB


blogAPI = FastAPI(debug=True)

blogAPI.mount('/', GraphQL(schema, debug=True))


SEPARATOR = '---------------'


@blogAPI.on_event('startup')
async def startup():
    print(SEPARATOR)
    print('STATUS: Connecting to database...')
    try:
        await MAIN_DB.connect()
    except Exception:
        print(f'ERROR: Database could not disconnect. {Exception}.')
        print(SEPARATOR)
    else:
        assert MAIN_DB.is_connected
        print('SUCCESS: Database connected.')
        print(f'You are now connected to {DB_NAME}')
        print(SEPARATOR)


@blogAPI.on_event('shutdown')
async def db_shutdown():
    print(SEPARATOR)
    print('STATUS: Disconnecting from database.')
    try:
        await MAIN_DB.disconnect()
    except Exception:
        print(f'ERROR: Database could not disconnect. {Exception}')
        print(SEPARATOR)
    else:
        assert not MAIN_DB.is_connected
        print('SUCCESS: Database disconnected.')
