import typing
from ..utils.custom_errors import TooManyColumnArguments, DataValidationError

from sqlalchemy import Table, select, column, and_
from databases import Database

from .main import DB
from .models import tbl_author

from ..utils.account import Account
from ..utils.database import is_data_valid


async def get_one_author(cols: list, where_val: dict, DB: Database = DB, table: Table = tbl_author) -> typing.Optional[typing.Mapping]:
    """
    Function to select one author from the Author relation. It uses cols (a list
    of SQLAlchemy Column type elements) to be able to fetch only the attributes
    in the list. The argument 'where_val' is a dictionary with only one key and
    value. It will only return authors that have the 'ACTIVE' status.
    
    EXAMPLE:

    cols = [my_table.c.my_column] or col = [my_table] if all columns are needed.

    where_val = {'id': 'my_id'}
    """

    keys_no = len(where_val.keys())
    if keys_no > 1:
        raise TooManyColumnArguments(
            f'Only one column is allowed. You have used {keys_no}.'
        )
    else:
        wh_key = list(where_val.keys())[0]
        wh_val = where_val[wh_key]
        wh_col = column(wh_key)
        _query = select(cols).where(and_(wh_col == wh_val, table.c.account_status == 'ACTIVE'))
        result = await DB.fetch_one(_query)
        return result 



async def new_author(insert_data: dict, DB: Database = DB, table: Table = tbl_author):
    
    _data = insert_data
    conf_password = 'conf_password'
    author = Account()

    try:
        is_data_valid(_data)
    except:
        raise DataValidationError
    else:
        _data.pop(conf_password)
        h_password = author.hash_password(_data['password'])
        _data['password'] = h_password
            ################! set it to not active when ready to validate email 
        # update the status of the account
        status = author.set_status('ACTIVE')
        stat_data = {'account_status': status}
        _data.update(stat_data)

        insert_q = table.insert().values(_data)
        transaction = DB.transaction()
        try:
            await transaction.start()
            result = await DB.execute(insert_q)
        except Exception:
            await transaction.rollback()
        else:
            await transaction.commit()
            return result