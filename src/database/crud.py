"""

"""


import typing
from databases import Database
from sqlalchemy import Table, select, and_
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.schema import Column
from .main import MAIN_DB
from .models import (
    tbl_account_artist,
    tbl_account_user,
    tbl_story,
    tbl_artist_story,
    tbl_artist_profile
)


DBColumnList = typing.List[Column]
DBTableList = typing.List[Table]


class MainDB:

    def __init__(
            self,
            is_test: bool = False,
            database: Database = MAIN_DB
    ) -> None:

        self.is_test = is_test
        self.DB = database

    def start_transaction(self):

        return self.DB.transaction()

    def execute(self, query, value=None):

        return self.DB.execute(query, value)

    async def fetch_one(
            self,
            cols: typing.Union[DBColumnList, DBTableList],
            where_clause: BooleanClauseList
    ) -> typing.Optional[typing.Mapping]:

        _query = select(cols).where(where_clause)
        result = await self.DB.fetch_one(_query)
        return result


class AccountDB(MainDB):

    def __init__(
            self,
            account_type: str,
            is_test: bool = False,
            database: Database = MAIN_DB
    ) -> None:

        super().__init__(is_test, database)
        self.table = self.get_table(account_type)

    @staticmethod
    def get_table(account_type):

        account_tables = {
            'artist': tbl_account_artist,
            'user': tbl_account_user
        }
        table = account_tables[account_type]
        return table

    async def fetch_all(
            self,
            cols: typing.Union[DBColumnList, DBTableList]
    ) -> typing.List[typing.Mapping]:

        # ! Make a limit and offset query. Maybe use cursor for this
        _query = select(cols).where(
            self.table.c.account_artist_status == 'active'
        )
        result = await self.DB.fetch_all(_query)
        return result

    async def create_account(
            self,
            account_data: dict
    ) -> typing.Optional[str]:

        insert_q = self.table.insert().values(account_data)
        result = await self.DB.execute(insert_q)
        return result


class ArtistDB(AccountDB):

    def __init__(self, is_test: bool = False) -> None:

        super().__init__('artist', is_test)
        self.table = tbl_account_artist
        self.attrib_prefix = self.table.name

    async def fetch_story_artist(
            self,
            cols: typing.Union[DBColumnList, DBTableList],
            where_clause: typing.Dict[str, str]
    ) -> typing.Optional[typing.List]:
        """

        Args:
            cols:
            where_clause:

        Returns:

        """

        join_q = self.table.\
            join(tbl_artist_story,
                 self.table.c.account_artist_id == tbl_artist_story.c.artist_id_fk
                 ).\
            join(tbl_story,
                 tbl_story.c.story_id == where_clause['story_id']
                 )
        _query = select(cols, distinct=True).select_from(join_q)
        result = await self.DB.fetch_all(_query)

        return result


class UserDB(AccountDB):

    def __init__(self, is_test: bool = False) -> None:

        super().__init__('user', is_test)
        self.table = tbl_account_user
        self.attrib_prefix = self.table.name


class ArtistProfileInformationDB(MainDB):
    def __init__(
            self,
            is_test: bool = False,
            database: Database = MAIN_DB
    ) -> None:
        super().__init__(is_test, database)
        self.table = tbl_artist_profile
        self.attribute_prefix = 'artist'


class StoryDB(MainDB):

    def __init__(self, is_test: bool = False) -> None:
        super().__init__(is_test)
        self.table = tbl_story
        self.attribute_prefix = self.table.name

    async def fetch_artist_stories(
            self,
            cols: typing.Union[DBColumnList, DBTableList],
            where_clause_val: typing.Dict[str, str]
    ) -> typing.Optional[typing.List]:
        """
        """

        join_q = self.table.\
            join(tbl_artist_story,
                 self.table.c.story_id ==
                 tbl_artist_story.c.story_id_fk
                 ).\
            join(tbl_account_artist,
                 tbl_artist_story.c.artist_id_fk ==
                 tbl_account_artist.c.account_artist_id
                 )
        where_clause = and_(
            tbl_account_artist.c.account_artist_id ==
            where_clause_val['artist_id'],
            tbl_account_artist.c.account_artist_status == 'active'
        )
        _query = select(cols).select_from(join_q).where(where_clause)
        result = await self.DB.fetch_all(_query)
        return result

    async def create_story(self, story_data: dict) -> typing.Optional[str]:

        insert_q = self.table.insert().values(story_data)
        result = await self.DB.execute(insert_q)
        return result
