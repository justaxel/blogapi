from inspect import BoundArguments


class BaseError(Exception):
    """Base class for other custom exceptions"""
    pass


class NotAllowedCharacter(BaseError):
    """Raised when the input value is not allowed."""
    pass


class AccountAlreadyExists(BaseError):
    pass


class CouldNotLoadFile(BaseError):
    pass


class MaxNumberOfCharactersReached(BaseError):
    pass


class TooManyColumnArguments(BaseError):
    pass


class TooManyWhereClauseAttributes(BaseError):
    pass


class EmptyPasswordNotAllowed(BaseError):
    pass


class NoDataFound(BaseError):
    pass


class SomeDataMightBeEmpty(BaseError):
    pass


class DataValidationError(BaseError):
    pass


class WrongAccountType(BaseError):
    pass


class PasswordsDoNotMatch(BaseError):
    pass


class EmptyValue(BaseError):
    pass
