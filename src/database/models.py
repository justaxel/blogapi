from sqlalchemy import (
    Table, Column, text,
    String, Text, DateTime, Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

from .main import metadata


tbl_account_author = Table(
    'account_author', metadata,
    Column('account_author_id', UUID, primary_key=True, server_default=text('gen_random_uuid()')),
    Column('account_author_username', String(250), nullable=False, unique=True),
    Column('account_author_email', Text, nullable=False, unique=True),
    Column('account_author_status', Text, nullable=False),
    Column('account_author_password', String(15), nullable=False),
    Column('account_author_date_created', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('account_author_date_modified', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
)


tbl_author_profile = Table(
    'profile_author', metadata,
    Column('author_id_fk', ForeignKey('account_author.id', ondelete='CASCADE', onupdate='CASCADE')),
    Column('author_name_first', String(50)),
    Column('author_name_last', String(50)),
    Column('author_bio_descript', String(250)),
    Column('author_location', String(30))
)


tbl_story = Table(
    'story', metadata,
    Column('story_id', UUID, primary_key=True, server_default=text("gen_random_uuid()")),
    Column('story_title', String(286), nullable=False, unique=True),
    Column('story_synopsis', Text),
    Column('story_content', Text),
    Column('story_date_created', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('story_date_modified', DateTime(True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
    Column('story_is_published', Boolean, nullable=False, server_default=text("false")),
    Column('story_language', String(3)),
    Column('story_uri', String(2000), nullable=False)
)


tbl_author_story = Table(
    'author_story', metadata,
    Column('author_id_fk', ForeignKey('account_author.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False),
    Column('story_id_fk', ForeignKey('story.id', ondelete='CASCADE', onupdate='CASCADE'), primary_key=True, nullable=False)
)