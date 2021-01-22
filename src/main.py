from fastapi import FastAPI
from ariadne.asgi import GraphQL
from .gql.type_def import schema

from .settings import DB_NAME
from .database.main import DB


blogAPI = FastAPI(debug=True)
blogAPI.mount('/', GraphQL(schema, debug=True))


SEPARATOR = '---------------'


@blogAPI.on_event('startup')
async def startup():
    print(SEPARATOR)
    print('STATUS: Connecting to database...')
    try:
        await DB.connect()
    except:
        print('ERROR: Database could not connect.')
        print(SEPARATOR)
    else:
        assert DB.is_connected
        print('SUCCESS: Database connected.')
        print(f'You are now connected to {DB_NAME}')
        print(SEPARATOR)
        

@blogAPI.on_event('shutdown')
async def db_shutdown():
    print(SEPARATOR)
    print('STATUS: Disconnecting from database.')
    try:
        await DB.disconnect()
    except:
        print('ERROR: Database could not disconnect.')
        print(SEPARATOR)
    else:
        assert not DB.is_connected
        print('SUCCESS: Database disconnected.')
