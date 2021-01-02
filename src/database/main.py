import databases
from ..settings import DB_URL


DB = databases.Database(DB_URL)

