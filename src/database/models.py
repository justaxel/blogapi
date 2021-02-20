from sqlalchemy import (
    Table, Column, text,
    String, Text, DateTime, Boolean,
    ForeignKey
)
from sqlalchemy.dialects.postgresql import UUID

from .main import metadata


tbl_account_artist = Table(
    'account_artist', metadata,
    Column('account_artist_id', UUID,
           primary_key=True, server_default=text('gen_random_uuid()')
           ),
    Column('account_artist_username', String(250),
           nullable=False, unique=True
           ),
    Column('account_artist_email', Text, nullable=False, unique=True),
    Column('account_artist_status', Text, nullable=False),
    Column('account_artist_password', String(15), nullable=False),
    Column('account_artist_date_created', DateTime(True),
           nullable=False, server_default=text("CURRENT_TIMESTAMP")
           ),
    Column('account_artist_date_modified', DateTime(True),
           nullable=False, server_default=text("CURRENT_TIMESTAMP")
           )
)


tbl_artist_profile = Table(
    'profile_artist', metadata,
    Column('artist_id_fk', ForeignKey(
        'account_artist.id', ondelete='CASCADE', onupdate='CASCADE'
    )),
    Column('artist_name_first', String(50)),
    Column('artist_name_last', String(50)),
    Column('artist_bio_descript', String(250)),
    Column('artist_location', String(30))
)


tbl_story = Table(
    'story', metadata,
    Column('story_id', UUID,
           primary_key=True, server_default=text("gen_random_uuid()")
           ),
    Column('story_title', String(286), nullable=False, unique=True),
    Column('story_synopsis', Text),
    Column('story_content', Text),
    Column('story_date_created', DateTime(True),
           nullable=False, server_default=text("CURRENT_TIMESTAMP")
           ),
    Column('story_date_modified', DateTime(True),
           nullable=False, server_default=text("CURRENT_TIMESTAMP")
           ),
    Column('story_is_published', Boolean,
           nullable=False, server_default=text("false")
           ),
    Column('story_language', String(3)),
    Column('story_uri', String(2000), nullable=False)
)


tbl_artist_story = Table(
    'artist_story', metadata,
    Column('artist_id_fk', ForeignKey(
        'account_artist.id', ondelete='CASCADE', onupdate='CASCADE'
    ), primary_key=True, nullable=False),
    Column('story_id_fk', ForeignKey(
        'story.id', ondelete='CASCADE', onupdate='CASCADE'
    ), primary_key=True, nullable=False)
)
