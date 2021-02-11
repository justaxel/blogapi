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


def dict_keys_to_camel_case(old_dict: dict) -> dict:
    """Turns every dictionary key into camel case."""

    new_dict = {to_camel_case(key): value for key, value in old_dict.items()}
    return new_dict


def clean_query_attribs(query_attribs: str) -> typing.List[str]:
    """

    Args:
        query_attribs:

    Returns:

    """
    clean_attribs = re.split(r"[\W]+", query_attribs)
    attribs = [to_snake_case(attrib) for attrib in clean_attribs if attrib != '']
    return attribs
