import re
import typing
from passlib.hash import argon2

from .custom_errors import (
    CouldNotHashPassword,
    MaxNumberOfCharactersReached,
    EmptyPasswordNotAllowed
)


class Account:

    def hash_password(self, password: str) -> str:
        """Returns an hashed string using Argon2id functionality."""
    
        if len(password) > 0: 
            try:
                hashed_str = argon2.hash(password)
            except:
                raise CouldNotHashPassword
            else:
                return hashed_str
        else:
            raise EmptyPasswordNotAllowed
    
    def verify_password(self, raw_password: str, hashed_str: str) -> bool:
        """Verifies if a string matches a given hashed string."""

        return argon2.verify(raw_password, hashed_str)
    
    def is_username_valid(self, username: str) -> bool:
        """
        Returns True if and only if it is made up of 250 characters or less,
        all of which are composed by letters a-Z (lowercase and uppercase),
        numbers 0-9 and underscores. Returns a MaxNumberOfCharactersReached or TypeError otherwise.
        """

        MAX_CHARS_NO = 250

        len_username = len(username)
        if len_username > MAX_CHARS_NO:
            raise MaxNumberOfCharactersReached((
                'The username can only be 250 or less characters long. '
                f'The one provided has: {len_username} characters.'
            ))
        elif len_username > 0 and len_username <= MAX_CHARS_NO:
            search_badchar = re.search(r"\W", username)
            if search_badchar is not None:
                raise TypeError((
                    'The username can only contain letters (a-Z), numbers (0-9) and underscores. '
                    f'Please check your input: {username}.'
                ))
            else:
                return True
        else:
            return False
    
    def set_status(self, status: str) -> str:
        """
        Set the status of an Account instance. The only options are: 'ACTIVE', 'NOT ACTIVE', and 'DELETED'.
        """

        STATUS_OPTS = ['ACTIVE', 'NOT ACTIVE', 'DELETED']
        new_status = status.upper()
        if new_status in STATUS_OPTS:
            return new_status
        else:
            raise NameError((
                f'{status} is not a valid status. '
                f"Please use one of the following status options: '{', '.join(STATUS_OPTS)}'."
            ))
