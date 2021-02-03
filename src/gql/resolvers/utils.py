import re
import typing


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


def remove_table_prefix_from_dict(old_dict: dict, tbl_prefix: str) -> dict:
    
    new_dict = {key.replace(tbl_prefix, ''): value for key, value in old_dict.items()}
    return new_dict


def dict_keys_to_camel_case(old_dict: dict) -> dict:
    """Turns every dictionary key into camel case."""

    new_dict = {to_camel_case(key): value for key, value in old_dict.items()}
    return new_dict
