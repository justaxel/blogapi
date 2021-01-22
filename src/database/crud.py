import typing
from databases import Database
from sqlalchemy import Table, select, column, and_
from sqlalchemy.sql.elements import BooleanClauseList
from sqlalchemy.sql.schema import Column

from .main import DB
from .models import tbl_account_author

from ..utils.custom_errors import (
    TooManyColumnArguments,
    WrongAccountType
)


class AccountDB:
    """
    A class to read, create, update, and delete accounts.

    Attributes
    ----------
    `account_type` : str
        The type of the account.
    
    Methods
    -------
    `get_table()`:
        Gets and assings the correct account table for the `account_type` specified.
        No need to call it, since this function it's called by the class
        constructor.

    `fetch_one()`:
        Gets only one account according to the specified table attributes and values.
    
    `fetch_all()`:
        Gets all accounts according to the specified table attributes.

    `create_account()`:
        Creates a new account.
    """

    def __init__(self, account_type: str, is_test: bool = False):
        self.account_type = account_type
        self.is_test = is_test
        self.get_database()
        self.get_table()
    
    def get_database(self, database: typing.Optional[Database] = None) -> Database:

        MAIN_DATABASE = DB
        self.DB = MAIN_DATABASE
        if self.is_test is True:
            if database is not None:
                self.DB = database
        
        return self.DB
    
    def get_table(self) -> Table:
        """
        Assings the correct SQL Alchemy Table for the specified account type.
        In case `account_type` is not recognize, it will raise a `WrongAccountType`
        error. This functions is automatically called in the `AccountDB` constructor,
        so there is no need to call it separately.
        """

        ALL_ACCOUNT_TABLES = {
            'author': tbl_account_author,
            #'user': tbl_account_user 
        }
        try:
            self.table = ALL_ACCOUNT_TABLES[self.account_type]
        except KeyError:
            raise WrongAccountType
        else:
            return self.table
    
    def start_transaction(self):

        return self.DB.transaction()
    
    def execute(self, query, value = None):

        return self.DB.execute(query, value)
    
    async def fetch_one(
        self,
        cols: typing.Union[typing.List[Column], typing.List[Table]],
        where_clause: BooleanClauseList
    ) -> typing.Optional[typing.Mapping]:
        """
        Function to fetch a single account. It uses `cols` to be able to fetch only
        the attributes specified in the list or the entire table attributes.
        The argument `where_val` can only have one key and value.
        The function will only return active accounts.

        EXAMPLE
        -------
        `cols = [my_table.c.my_column]` or `col = [my_table]`
        if all columns are needed, and

        `where_val = {'id': 'my_id'}`
        """

        _query = select(cols).where(where_clause)
        result = await self.DB.fetch_one(_query)
        return result


    async def fetch_all(
        self,
        cols: typing.Union[typing.List[Column], typing.List[Table]]
    ) -> typing.List[typing.Mapping]:
        """
        Fetch all active accounts. It uses `cols` to be able to fetch only
        the attributes specified in the list or the entire table attributes.

        EXAMPLE
        -------
        `cols = [my_table.c.my_column]` or `col = [my_table]`
        if all columns are needed.
        """

    #! Make a limit and offset query. Maybe use cursor for this
        _query = select(cols).where(self.table.c.account_status == 'active')
        result = await self.DB.fetch_all(_query)
        return result


    async def create_account(self, account_data: dict) -> typing.Optional[str]:
        """
        Create an account based on the specified `account_data` dictionary.

        IMPORTANT
        ---------
        This function does not sanitize data. All data should be validated
        before calling `create_account`.
        """

        insert_q = self.table.insert().values(account_data)
        result = await self.DB.execute(insert_q)
        return result

