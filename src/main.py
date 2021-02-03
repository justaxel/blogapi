from fastapi import FastAPI, Request
from ariadne.asgi import GraphQL
from sqlalchemy.sql.schema import Column
from .gql.type_def import schema

from .settings import DB_NAME
from .database.main import DB

from .database.crud import StoryDB
from .database.models import tbl_story

blogAPI = FastAPI(debug=True)

blogAPI.mount('/', GraphQL(schema, debug=True))


SEPARATOR = '---------------'


@blogAPI.on_event('startup')
async def startup():
    print(SEPARATOR)
    print('STATUS: Connecting to database...')
    try:
        await DB.connect()
    except Exception:
        print(f'ERROR: Database could not disconnect. {Exception}.')
        print(SEPARATOR)
    else:
        assert DB.is_connected
        print('SUCCESS: Database connected.')
        print(f'You are now connected to {DB_NAME}')
        print(SEPARATOR)
        # s = StoryDB()
        # result = await s.fetch_author_stories([tbl_story], {'username': 'harrypotter80'})
        # _stories = [dict(story) for story in result]
        # print(_stories)


@blogAPI.on_event('shutdown')
async def db_shutdown():
    print(SEPARATOR)
    print('STATUS: Disconnecting from database.')
    try:
        await DB.disconnect()
    except Exception:
        print(f'ERROR: Database could not disconnect. {Exception}')
        print(SEPARATOR)
    else:
        assert not DB.is_connected
        print('SUCCESS: Database disconnected.')
