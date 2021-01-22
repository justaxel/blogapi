import typing
import re
from passlib.hash import argon2
from ..utils.custom_errors import (
    MaxNumberOfCharactersReached,
    NoDataFound,
    SomeDataMightBeEmpty
)


class AccountDataVerification():
    """
    A data checker for any class `Account` instance.

    Attributes
    ----------
    `account_data`: Dict[str, str]
        Data to be checked.

    Methods
    -------
    `is_username_valid(username)`
        Verifies if the username adheres to requirements.

    `is_data_valid()`
        Verifies if the `account_data` meets minimum requirements.

    `is_hashed_str_valid(raw_password, hashed_str)`
        Verifies if a given string matches another hashed string.
    """

    def __init__(self, account_data: typing.Dict[str, str]):
        """Constructor for the class `AccountDataVerificator`."""

        self.account_data = account_data
    
    def is_data_valid(self) -> bool:
        """
        Verifies if the the entire var `account_data` is valid.
        Returns True if and only if the  
        """

        REQUIRED_DATA = ['username', 'email', 'password', 'password_confirm']
        R_DATA_USERNAME = REQUIRED_DATA[0]
        R_DATA_PASSWORD = REQUIRED_DATA[2]
        R_DATA_PASSWORD_CONFIRM = REQUIRED_DATA[3]
        data = self.account_data

        # check that every field in required data is in the query_data AND
        # check that every value of every field is not empty.
        for field in REQUIRED_DATA:
            try:
                data[field]
            except KeyError as err_key:
                raise NoDataFound(
                    f"It appears that '{err_key}' might be missing. "
                    "Please check that you have all required data. "
                    f"Here is a hint: {', '.join(REQUIRED_DATA)}"
                )
            else:
                # if the value for the field is empty raise error
                if not data[field]:
                    raise SomeDataMightBeEmpty(
                        f"It appears that '{field}' field is empty. "
                        "Please check that all required data has a valid value"
                    )
        # check if username provided is valid
        try:
            self.is_username_valid(data[R_DATA_USERNAME])
        except Exception:
            return False
        else:
            if data[R_DATA_PASSWORD_CONFIRM] != data[R_DATA_PASSWORD]:
                return False
            return True

    def is_username_valid(self, username: str) -> bool:
        """
        Verifies if a given username is valid.
        Returns True if and only if it is made up of 250 characters or less,
        all of which are composed by letters a-Z (lowercase and uppercase),
        numbers 0-9 and unserscores '_'.
        """

        MAX_CHARS_NO = 250

        len_username = len(username)
        if len_username > MAX_CHARS_NO:
            raise MaxNumberOfCharactersReached(
                'A username can only be 250 or less characters long. '
               f"The one provided has '{len_username}' characters."
        )
        elif len_username > 0 and len_username <= MAX_CHARS_NO:
            search_bad_char = re.search(r"\W", username)
            if search_bad_char is not None:
                raise TypeError(
                    'The username can only contain letters (a-Z), numbers (0-9) and underscores. '
                    f'Please check your input: {username}.'
            )
            else:
                return True
        else:
            return False
        
    def is_hashed_str_valid(self, raw_password: str, hashed_str: str) -> bool:
        """Verifies if a string matches a given hashed string."""

        return argon2.verify(raw_password, hashed_str)
