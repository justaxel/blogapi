from typing import Dict
from passlib.hash import argon2
from ..database.crud import ArtistDB

from ..utils.custom_errors import (
    EmptyPasswordNotAllowed,
)


class Account:

    def __init__(
            self,
            username: str,
            email: str,
            password: str,
            status: str = 'not active'
    ) -> None:
        """
        Constructs all the basic and necessary attributes for an account object.
        """

        self.username = username
        self.email = email
        self.password = password
        self.status = self.set_status(status)
    
    def hash_password(self) -> str:
        """
        Hashes the Account's password.
        """

        if len(self.password) > 0:
            # generate new salt, hash password
            hashed_str = argon2.hash(self.password)
            self.password = hashed_str
            return hashed_str
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

    @staticmethod
    def set_status(self, status: str) -> str:
        """
        Sets the current status of the account. The options are established by
        ACCOUNTS_STATUS_OPTS constant:
        `active`, `not active`, `upon deletion`, and `deleted`.
        """

        account_status_opts = [
            'active',
            'not active',
            'upon deletion',
            'deleted',
        ]
        _status = status.lower()
        if _status not in account_status_opts:
            raise ValueError(
                f'{status} is not a valid account status. '
                'Please see the status module to find all available account status'
            )
        else:
            status = _status
        return status


class Artist(Account):

    def __init__(
            self,
            username: str,
            email: str,
            password: str,
            status: str = '',
            is_test: bool = False
    ) -> None:

        super().__init__(username, email, password, status)
        self._db = ArtistDB(is_test)

    @property
    def db(self):
        return self._db
