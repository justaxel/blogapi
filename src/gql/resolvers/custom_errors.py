class BaseError(Exception):
    """Base class for other custom Exceptions"""
    pass


class QueryIsNotAString(BaseError):
    
    pass


class NumberOfQueryAttributesDoNotMatch(BaseError):
    pass


class TooManyWhereClauseAttributes(BaseError):
    pass