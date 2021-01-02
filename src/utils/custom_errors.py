class BaseError(Exception):
    """Base class for other custom exceptions"""
    pass


class NotAllowedCharacter(BaseError):
    """Raised when the input value is not allowed."""
    pass


class AccountAlreadyExists(BaseError):
    pass


class CouldNotHashPassword(BaseError):
    pass


class CouldNotLoadFile(BaseError):
    pass


class MaxNumberOfCharactersReached(BaseError):
    pass

