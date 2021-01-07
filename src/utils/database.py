from .account import Account
from .custom_errors import NoDataFound, SomeDataMightBeEmpty


def get_db_data(db_data: str , is_test: bool = False) -> str:
    
    if is_test:
        request = f'TEST_{db_data}'
    else:
        request = f'{db_data}'
    return request


def is_data_valid(data: dict) -> bool:

    REQUIRED_DATA = ['username', 'email', 'password', 'conf_password']

    if not data:
        return False
    for field in REQUIRED_DATA:
        try:
            data[field]
        except KeyError as e:
            raise NoDataFound(
                f"It appears that {e} might be missing. "
                "Please check that you have input all required data."
        )
        else:
            if not data[field]:
                raise SomeDataMightBeEmpty(
                    f"It appears that \"{field}\" field is empty. "
                    "Please check that all required data has a valid value"
                )
    
    account = Account()
    try:
        account.is_username_valid(data['username'])
    except Exception:
        return False
    else:
        if data['password'] != data['conf_password']:
            return False
        return True
