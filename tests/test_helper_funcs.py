import pytest

from ..src.utils.helper_funcs import (
    to_camel_case,
    to_snake_case,
    dict_keys_to_camel_case,
    get_query_fields
)
from ..src.utils.custom_errors import QueryIsNotAString, NoQueryName


def test_to_camel_case():
    string1 = '_this_is_my_string_12'
    assert to_camel_case(string1) == 'thisIsMyString12'
    string2 = ''
    assert to_camel_case(string2) == ''

def test_to_snake_case():
    string1 = 'thisIsMyString12'
    assert to_snake_case(string1) == 'this_is_my_string12'
    string2 = ''
    assert to_snake_case(string2) == ''

def test_dict_keys_to_camel_case():
    dict1 = {
        'my_key': 'val1',
        'another_key_12': 'val2',
        '_one_more_key': 'val3'
    }
    assert dict_keys_to_camel_case(dict1) == {
        'myKey': 'val1',
        'anotherKey12': 'val2',
        'oneMoreKey': 'val3'
    }

def test_get_query_fields():
    query_with_args = ('query getOneAuthor {\n  author(username: "harrypotter80") {\n    id\n    username\n    email\n    accountStatus\n    dateCreated\n  }\n}\n')
    final_query_list = ['id', 'username', 'email', 'account_status', 'date_created']
    assert get_query_fields(query_with_args) == final_query_list
    query_no_args = ('query getOneAuthor {\n  authors {\n    id\n    username\n    email\n    accountStatus\n    dateCreated\n  }\n}\n')
    assert get_query_fields(query_no_args, 'author') == final_query_list
    with pytest.raises(NoQueryName) as e_info:
        get_query_fields(query_no_args)
        assert str(e_info.value) == 'Please provide the name of your query.'