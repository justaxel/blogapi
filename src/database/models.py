from sqlalchemy import (
    Table, Column, MetaData, text,
    String, Text, DateTime
)
from sqlalchemy.dialects.postgresql import UUID
from .main import engine


metadata = MetaData(engine)

tbl_author = Table(
    'author', metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('username', String(250), nullable=False, unique=True),
    Column('email', Text, nullable=False, unique=True),
    Column('account_status', Text, nullable=False),
    Column('password', String(15), nullable=False),
    Column('date_created', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('date_modified', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)
