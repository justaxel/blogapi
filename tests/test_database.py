import pytest
import databases
from os import getenv
import sqlalchemy
from sqlalchemy.dialects.postgresql import UUID

from src.utils.custom_errors import (
    TooManyColumnArguments,
    SomeDataMightBeEmpty,
    DataValidationError
)
from src.settings import BASE_DIR
from src.settings import _load_dotenv

from src.database.crud import AccountDB


################# BEGINNING OF FIXTURES #################


@pytest.fixture
def get_db_url():
    
    _load_dotenv(BASE_DIR)
    T_DB_NAME = getenv('TEST_DATABASE_NAME')
    T_DB_HOST = getenv('TEST_DATABASE_HOST')
    T_DB_USER = getenv('TEST_DATABASE_USER')
    T_DB_PWRD = getenv('TEST_DATABASE_PWRD')
    T_DB_URL = f'postgresql://{T_DB_USER}:{T_DB_PWRD}@{T_DB_HOST}/{T_DB_NAME}'
    #print(T_DB_URL)
    return T_DB_URL

@pytest.fixture
def setup_test_database(get_db_url):

    TEST_DB = databases.Database(get_db_url)
    return TEST_DB

@pytest.fixture
def get_test_database_metadata(get_db_url):
    
    TEST_engine = sqlalchemy.create_engine(get_db_url)
    TEST_metadata = sqlalchemy.MetaData(TEST_engine)
    return TEST_metadata

@pytest.fixture
def setup_test_database_account_author_model(get_test_database_metadata):

    metadata = get_test_database_metadata
    Column = sqlalchemy.Column

    TEST_tbl_account_author = sqlalchemy.Table(
    'account_author', metadata,
    Column('id', UUID, primary_key=True, server_default=sqlalchemy.text('gen_random_uuid()')),
    Column('username', sqlalchemy.String(250), nullable=False, unique=True),
    Column('email', sqlalchemy.Text, nullable=False, unique=True),
    Column('account_status', sqlalchemy.Text, nullable=False),
    Column('password', sqlalchemy.String(15), nullable=False),
    Column('date_created', sqlalchemy.DateTime(True), nullable=False, server_default=sqlalchemy.text("CURRENT_TIMESTAMP")),
    Column('date_modified', sqlalchemy.DateTime(True), nullable=False, server_default=sqlalchemy.text("CURRENT_TIMESTAMP"))
    )
    return TEST_tbl_account_author

@pytest.fixture
def db_test_account_author_instance(setup_test_database_account_author_model):

    TEST_account_author = AccountDB('author', is_test=True)
    return TEST_account_author


#################### END OF FIXTURES ####################

@pytest.mark.asyncio
async def test_db_startup(setup_test_database):

    T_DB = setup_test_database
    await T_DB.connect()
    assert T_DB.is_connected
    await T_DB.disconnect()
    assert not T_DB.is_connected

@pytest.mark.asyncio
async def test_db_author_query(
    setup_test_database,
    setup_test_database_account_author_model,
    db_test_account_author_instance,
):

    from uuid import UUID
    from sqlalchemy import and_

    T_DB = setup_test_database    
    T_account_author = db_test_account_author_instance
    T_account_author.get_database(setup_test_database)
    T_account_author.table = setup_test_database_account_author_model

    await T_DB.connect()
    assert T_DB.is_connected

    T_tbl_account_author = setup_test_database_account_author_model    
    cols = [T_tbl_account_author]
    where_clause_by_username = and_(
        T_tbl_account_author.c.username == 'harrypotter80',
        T_tbl_account_author.c.account_status == 'active'
    )

    author = await T_account_author.fetch_one(cols, where_clause_by_username)
    assert author['id'] == UUID('37941b34-9026-4a09-802c-2616210cb1c2')

    where_clause_by_wrong_username = and_(
        T_tbl_account_author.c.username == 'NotAUsernameInDB',
        T_tbl_account_author.c.account_status == 'active'
    )
    not_an_author = await T_account_author.fetch_one(cols, where_clause_by_wrong_username)
    assert not_an_author is None

    with pytest.raises(TypeError) as e_info:
        await T_account_author.fetch_one(cols)
    assert str(e_info.value) == "fetch_one() missing 1 required positional argument: 'where_clause'"

    await T_DB.disconnect()
    assert not T_DB.is_connected

#@pytest.mark.asyncio
#async def test_db_author_insert(setup_testDB, db_author_model):
#
#    from asyncpg.pgproto.pgproto import UUID as pgUUID
#