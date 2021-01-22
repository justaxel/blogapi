from sqlalchemy import (
    Table, Column, text,
    String, Text, DateTime, Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

from .main import metadata


tbl_account_author = Table(
    'account_author', metadata,
    Column('id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('username', String(250), nullable=False, unique=True),
    Column('email', Text, nullable=False, unique=True),
    Column('account_status', Text, nullable=False),
    Column('password', String(15), nullable=False),
    Column('date_created', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('date_modified', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)


tbl_story = Table(
    'story', metadata,
    Column('id', UUID, primary_key=True, server_default=text("gen_random_uuid()")),
    Column('title', String(286), nullable=False, unique=True),
    Column('content', Text),
    Column('date_created', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('date_modified', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('is_published', Boolean, nullable=False, server_default=text("false")),
    Column('language_iso_6392', String(3))
)


tbl_author_story = Table(
    'author_story', metadata,
    Column('author_id', ForeignKey('account_author.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('story_id', ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
)