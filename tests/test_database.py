import datetime
import pytest
import databases
import sqlalchemy

from os import getenv
from sqlalchemy.dialects.postgresql import UUID as sqlalchemyUUID
from uuid import UUID
from asyncpg.pgproto.pgproto import UUID as pgUUID

from src.utils.custom_errors import (
    TooManyColumnArguments,
    SomeDataMightBeEmpty,
    DataValidationError
)

from src.settings import BASE_DIR
from src.settings import _load_dotenv
from src.database.crud import AccountDB
from src.database.verification import AccountDataVerification
from src.classes.accounts import Author


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

    TEST_DB = databases.Database(get_db_url, force_rollback=True)
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
    Column('id', sqlalchemyUUID, primary_key=True, server_default=sqlalchemy.text('gen_random_uuid()')),
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


################# BEGINNING OF TESTS ####################


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

    T_DB = setup_test_database    
    T_account_author = db_test_account_author_instance
    T_account_author.get_database(setup_test_database)
    T_account_author.table = setup_test_database_account_author_model

    await T_DB.connect()
    assert T_DB.is_connected

    all_cols = [T_account_author.table]
    where_clause_by_username = sqlalchemy.and_(
        T_account_author.table.c.username == 'harrypotter80',
        T_account_author.table.c.account_status == 'active'
    )

    author1 = await T_account_author.fetch_one(all_cols, where_clause_by_username)
    assert author1['id'] == UUID('37941b34-9026-4a09-802c-2616210cb1c2')
    assert author1['username'] == 'harrypotter80'
    assert author1['email'] == 'harrypotter80@email.com'
    assert author1['account_status'] == 'active'
    assert not author1['password'] == 'ItsHarryPotterBitch'

    some_cols = [
        T_account_author.table.c.id,
        T_account_author.table.c.username,
        T_account_author.table.c.email,
        T_account_author.table.c.date_created
    ]

    some_cols2 = [
        sqlalchemy.Column('id'),
        sqlalchemy.Column('username'),
        sqlalchemy.Column('email'),
        sqlalchemy.Column('date_created')
    ]

    author2 = await T_account_author.fetch_one(some_cols, where_clause_by_username)
    assert author1['id'] == UUID('37941b34-9026-4a09-802c-2616210cb1c2')
    assert author2['username'] == 'harrypotter80'
    assert author2['email'] == 'harrypotter80@email.com'
    assert author2['date_created'] == datetime.datetime.fromisoformat('2021-01-22 09:21:25.553587+00:00')

    author3 = await T_account_author.fetch_one(some_cols2, where_clause_by_username)
    assert author3['id'] == UUID('37941b34-9026-4a09-802c-2616210cb1c2')
    assert author3['username'] == 'harrypotter80'
    assert author3['email'] == 'harrypotter80@email.com'
    assert author2['date_created'] == datetime.datetime.fromisoformat('2021-01-22 09:21:25.553587+00:00')
    
    where_clause_by_wrong_username = sqlalchemy.and_(
        T_account_author.table.c.username == 'NotAUsernameInDB',
        T_account_author.table.c.account_status == 'active'
    )
    not_an_author = await T_account_author.fetch_one(all_cols, where_clause_by_wrong_username)
    assert not_an_author is None
    with pytest.raises(TypeError) as e_info:
        not_an_author['id']
    assert str(e_info.value) == "'NoneType' object is not subscriptable"

    with pytest.raises(TypeError) as e_info:
        await T_account_author.fetch_one(all_cols)
    assert str(e_info.value) == "fetch_one() missing 1 required positional argument: 'where_clause'"

    await T_DB.disconnect()
    assert not T_DB.is_connected


@pytest.mark.asyncio
async def test_db_author_insert(
    setup_test_database,
    db_test_account_author_instance,
    setup_test_database_account_author_model
):

    

    T_DB = setup_test_database     

    T_new_author_username = 'iamanewauthor'
    T_new_author_email = 'iamanewauthor@email.com'
    T_new_author_password = 'thisismysuperdupersecurepassword123'
    T_new_author_password_confirm = 'thisismysuperdupersecurepassword123'

    # this is the best case scenario data
    T_new_author_data = {
        'username': T_new_author_username,
        'email': T_new_author_email,
        'password': T_new_author_password,
        'password_confirm': T_new_author_password_confirm
    }

    verify_new_author_data = AccountDataVerification(T_new_author_data)
    
    # new_author_data should always be valid.
    assert verify_new_author_data.is_data_valid() is True
    
    T_new_author = Author(T_new_author_username, T_new_author_email, T_new_author_password, is_test=True)
    T_new_author._db.get_database(setup_test_database)
    T_new_author._db.table = setup_test_database_account_author_model
    T_table = T_new_author._db.table

    # build a where clause that will never return an existing author
    where_clause = sqlalchemy.or_(
        T_table.c.username == T_new_author_username,
        T_table.c.email == T_new_author_email
    )
    
    await T_DB.connect()
    assert T_DB.is_connected
    
    # this should never return any other value than None.
    not_an_existing_author = await T_new_author._db.fetch_one([T_table.c.id], where_clause)
    assert not_an_existing_author is None

    T_new_author.set_status('active')
    assert T_new_author.status == 'active'

    T_new_author.hash_password()
    assert not T_new_author.password == T_new_author_data['password']

    T_new_author_clean_data = T_new_author.spew_out_data()
    assert not T_new_author_clean_data == T_new_author_data

    # the following should not raise any exception.
    # for that reason it is not contained in a try/except/else logic.

    result = await T_new_author._db.create_account(T_new_author_clean_data)
    assert not result is None
    # the result from the create_account function should always return an id
    # of type UUID (or in this case, pgUUID)
    assert type(result) == pgUUID
    
    await T_DB.disconnect()
    assert not T_DB.is_connected
