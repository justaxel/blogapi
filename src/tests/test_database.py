import pytest
import databases
from os import getenv

from ..settings import BASE_DIR
from ..utils.database import get_db_data
from ..settings import _load_dotenv

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
    TEST_DB = databases.Database(get_db_url, force_rollback=True)
    return TEST_DB

#################### END OF FIXTURES ####################

@pytest.mark.asyncio
async def test_db_startup(setup_testDB):
    T_DB = setup_testDB
    await T_DB.connect()
    assert T_DB.is_connected
    await T_DB.disconnect()
    assert not T_DB.is_connected
