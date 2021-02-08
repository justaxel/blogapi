import databases
import sqlalchemy

from ..settings import DB_URL


MAIN_DB = databases.Database(DB_URL)

engine = sqlalchemy.create_engine(DB_URL)
metadata = sqlalchemy.MetaData(engine)