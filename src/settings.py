from os import path, getenv
from pathlib import Path
from dotenv import load_dotenv

from .utils.database import get_db_data

BASE_DIR = Path(__file__).resolve().parent.parent

def _load_dotenv(_path: Path):
    dotenv_path = path.join(_path, '.env')
    load_dotenv(dotenv_path)


_load_dotenv(BASE_DIR)

DB_NAME = getenv(get_db_data('DATABASE_NAME'))
DB_HOST = getenv(get_db_data('DATABASE_HOST'))
DB_USER = getenv(get_db_data('DATABASE_USER'))
DB_PWRD = getenv(get_db_data('DATABASE_PWRD'))

DB_URL = f'postgresql://{DB_USER}:{DB_PWRD}@{DB_HOST}/{DB_NAME}'

