class BaseError(Exception):
    """Base class for other custom Exceptions"""
    pass


class QueryIsNotAString(BaseError):
    
    pass


class NoRootQueryNameForGraphQLQueryWithNoArgs(BaseError):
    """
    Raised when :function:`get_gql_queries(query, has_args=False,
    query_name=None)` keyword argument `has_args` has been set to
    `False` but keyword argument `query_name` is `None`.
    """
    pass


class NumberOfQueryAttributesDoNotMatch(BaseError):
    pass
