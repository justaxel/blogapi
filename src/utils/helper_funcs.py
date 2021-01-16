import typing
import re

from .custom_errors import QueryIsNotAString


def to_camel_case(old_string: str) -> str:
    """Turns a snake case string into camel case."""

    if len(old_string) > 0:
        _string = old_string.replace("-", " ").replace("_", " ").split()
        _string = _string[0] + ''.join(i.capitalize() for i in _string[1:])
        return _string
    else:
        return old_string

def to_snake_case(old_string: str) -> str:
    """Turns a camel case string into snake case."""

    if len(old_string) > 0:
        pattern = re.compile(r'(?<!^)(?=[A-Z])')
        _string = pattern.sub('_', old_string).lower()
        return _string
    else:
        return old_string

def dict_keys_to_camel_case(old_dict: dict) -> dict:
    """Turns every dictionary key into camel case."""

    new_dict = {to_camel_case(key): value for key, value in old_dict.items()}
    return new_dict

def get_query_fields(query: str, query_name: str = None) -> typing.List[str]:
    """
    Fetches query fields from a GraphQL request. If the query requires
    arguments, the name of the query `query_name` should be passed as an argument.
    """

    if isinstance(query, str):
        pattern_query_with_args = re.compile(r"\) \{\n")
        pattern_query_no_args = re.compile(r" \{\n")
        
        result = pattern_query_with_args.search(query)
        if result is None:
            result = pattern_query_no_args.search(query)
        try:
            result_index = result.span()[0]
        except AttributeError:
            raise AttributeError
        else:
            dirty_list = re.split(r'[\W]+', query[result_index:])
            query_fields = [to_snake_case(field) for field in dirty_list if field != '' and field != query_name]
            return query_fields
    else:
        raise QueryIsNotAString