from typing import Dict
from passlib.hash import argon2
from ..database.crud import AccountDB

from ..utils.custom_errors import (
    CouldNotHashPassword,
    EmptyPasswordNotAllowed,
    EmptyValue
)


class Account:
    """
    A class to represent an account.
    
    Attributes
    ----------
    `username`: str

    `email`: str

    `password`: str

    Methods
    -------
    `set_status(status)`:
        Assigns the status of an account.
    
    `hash_password():
        Hashes the password of the account.
    
    `spew_data():
        Returns account's data as a dictionary.
    """

    def __init__(self, username: str, email: str, password: str) -> None:
        """
        Constructs all the basic and necessary attributes for an account object.
        """

        self.username = username
        self.email = email
        self.password = password
    
    def set_status(self, status: str) -> str:
        """
        Sets the current status of the account. The options are:
        `active`, `not active`, and `deleted`.
        """

        STATUS_OPTS = ['active', 'not active', 'deleted']

        if not status:
            raise EmptyValue

        if status in STATUS_OPTS:
            self.status = status
            return self.status
        else:
            raise NameError(
                f'{status} is not a valid status. '
                 "Please use one of the following status options: " 
                f"'{', '.join(STATUS_OPTS)}'."
        )
    
    def hash_password(self) -> str:
        """
        Hashes the Account's password.
        """

        password = self.password
        if len(password) > 0:
            try:
                # generate new salt, hash password
                hashed_str = argon2.hash(password)
            except:
                raise CouldNotHashPassword
            else:
                self.password = hashed_str
                return self.password
        else:
            raise EmptyPasswordNotAllowed

    def spew_out_data(self) -> Dict[str, str]:
        """
        Returns a dictionary containing all the data necessary to insert
        a new account to the Database.
        """
        
        account_data = {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'account_status': self.status
        }
        return account_data


class Author(Account):
    """
    A class to represent an Author. It inherits the `Account` class.
    """

    def __init__(self, username: str, email: str, password: str, is_test: bool = False) -> None:
        """
        Constructs all the necessary attributes for the author object.
        Binds the `AccountDB` class into the `_db` attribute.
        """
        super().__init__(username, email, password)
        self.account_type = 'author'
        self._db = AccountDB(self.account_type, is_test)
