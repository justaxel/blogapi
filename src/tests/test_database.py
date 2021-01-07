from ..utils.custom_errors import (
    TooManyColumnArguments,
    SomeDataMightBeEmpty,
    DataValidationError
)

import pytest
import databases
from os import getenv
from sqlalchemy import (
    Table, Column, MetaData, text,
    String, Text,
)
from sqlalchemy.dialects.postgresql import UUID

from ..settings import BASE_DIR
from ..settings import _load_dotenv
from ..utils.database import get_db_data

from ..database.crud import (
    get_one_author, new_author
)
################# BEGINNING OF FIXTURES #################


@pytest.fixture
def get_db_url():
    
    #print(BASE_DIR)
    _load_dotenv(BASE_DIR)
    T_DB_NAME = getenv(get_db_data('DATABASE_NAME', is_test=True))
    T_DB_HOST = getenv(get_db_data('DATABASE_HOST', is_test=True))
    T_DB_USER = getenv(get_db_data('DATABASE_USER', is_test=True))
    T_DB_PWRD = getenv(get_db_data('DATABASE_PWRD', is_test=True))
    T_DB_URL = f'postgresql://{T_DB_USER}:{T_DB_PWRD}@{T_DB_HOST}/{T_DB_NAME}'
    #print(T_DB_URL)
    return T_DB_URL

@pytest.fixture
def setup_testDB(get_db_url):

    # notice the 'force_rollback=True' argument
    TEST_DB = databases.Database(get_db_url, force_rollback=True)
    return TEST_DB

@pytest.fixture
def db_author_model():

    metadata = MetaData()
    tbl_author = Table(
    'author', metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('username', String(250), nullable=False, unique=True),
    Column('email', Text, nullable=False, unique=True),
    Column('status_account', Text, nullable=False),
    Column('password', String(15), nullable=False)
    )
    return tbl_author


#################### END OF FIXTURES ####################

@pytest.mark.asyncio
async def test_db_startup(setup_testDB):

    T_DB = setup_testDB
    await T_DB.connect()
    assert T_DB.is_connected
    await T_DB.disconnect()
    assert not T_DB.is_connected

@pytest.mark.asyncio
async def test_db_author_query(setup_testDB, db_author_model):
    
    import uuid

    T_DB = setup_testDB
    _table = db_author_model

    await T_DB.connect()
    assert T_DB.is_connected

    _cols = [_table.c.id, _table.c.username, _table.c.email]
    all_cols = [_table]
    _where_val = {'username': 'edgysquirrel'}

    # test if we got the correct result from db
    # query by username
    author1 = await get_one_author(T_DB, _table, _cols, _where_val)
    assert not author1 is None
    assert dict(author1)['username'] == 'edgysquirrel'
    
    # query by email
    author2 = await get_one_author(T_DB, _table, all_cols, _where_val)
    assert not author2 is None
    assert dict(author2)['email'] == 'edgysquirrel@email.com'

    # test that function raises the correct error message when you try
    # to pass too many dictionary elements to it.
    many_where_args = {'username': 'edgysquirrel', 'email': 'edgysquirrel@email.com'}
    with pytest.raises(TooManyColumnArguments) as e_info:
        await get_one_author(T_DB, _table, all_cols, many_where_args)
        assert str(e_info.value) == (
            f'Only one column is allowed. You have used 2.'
        )
    # test that the response is None when not getting any data from db.
    # you can generate a pseudo-random id for testing by uncommenting the line below
    #my_id = uuid.uuid4()
    m_id = 'edb1439e-7301-4627-a630-eeab57dff411'
    not_val = {'id': m_id}
    not_author = await get_one_author(T_DB, _table, _cols, not_val)
    assert not_author is None


@pytest.mark.asyncio
async def test_db_author_insert(setup_testDB, db_author_model):

    from asyncpg.pgproto.pgproto import UUID as pgUUID


    T_DB = setup_testDB
    _table = db_author_model

    await T_DB.connect()
    assert T_DB.is_connected

    # control data with valid values.
    _author = {
        'username': 'iamanewauthor',
        'email': 'iamanewauthor@email.com',
        'password': 'ThisIsMyPassword123)=5$#',
        'conf_password': 'ThisIsMyPassword123)=5$#'
    }

    n_author = await new_author(T_DB, _table, _author)
    assert not n_author is None
    # check that the value returned by the new_author function is the id of the author.
    assert type(n_author) == pgUUID

    # existing authors currently on the test database.
    existing_author = {
        'username': 'hermione79',
        'email': 'hermione79@email.com',
        'password': "ThisIsMyPassword!$###1231$%/&",
        'conf_password': "ThisIsMyPassword!$###1231$%/&"
    }
    existing_author2 = {
        'username': 'harrypotter80',
        'email': 'harrypotter80@email.com',
        'password': "ThisIsMyPassword!$###1231$%/&",
        'conf_password': "ThisIsMyPassword!$###1231$%/&"
    }
    existing_author3 = {
        'username': 'RonWeasley80',
        'email': 'ronweasley80@email.com',
        'password': "ThisIsMyPassword!$###1231$%/&",
        'conf_password': "ThisIsMyPassword!$###1231$%/&"
    }

    # this should return violation of unique constraint (email)
    # you can play with all 'existing_author...' if you want
    # they all should return the same error.
    n_author = await new_author(T_DB, _table, existing_author3)
    assert n_author is None

    # new author has different email, but same username as other author
    author_with_existing_username = {
        'username': 'harrypotter80',
        'email': 'thisisanewemail@email.com',
        'password': 'myhackablepassword',
        'conf_password': 'myhackablepassword'
    }
    # this should return violation of unique contraint (username)
    n_author1 = await new_author(T_DB, _table, author_with_existing_username)
    assert n_author1 is None

    author_with_missing_email = {
        'username': 'idonothaveanemail',
        'email': '',
        'password': 'myhackablepassword2',
        'conf_password': 'myhackablepassword2'
    }
    with pytest.raises(DataValidationError):
        n_author2 = await new_author(T_DB, _table, author_with_missing_email)
        assert n_author2 is None

    author_with_missing_username = {
        'username': '',
        'email': 'idonothaveausername',
        'password': 'myhackablepassword3',
        'conf_password': 'myhackablepassword3'
    }
    with pytest.raises(DataValidationError):
        n_author3 = await new_author(T_DB, _table, author_with_missing_username)
        assert n_author3 is None

    author_with_missing_pwrds = {
        'username': 'avalidusername',
        'email': 'avalidusername@email.com',
        'password': '',
        'conf_password': ''
    }
    with pytest.raises(DataValidationError):
        n_author4 = await new_author(T_DB, _table, author_with_missing_pwrds)
        assert n_author4 is None
