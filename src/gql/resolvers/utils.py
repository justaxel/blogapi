import re
import typing
from databases.backends.postgres import Record


def from_snake_to_camel_case(snake_cased_string: str) -> str:
    """

    Args:
        snake_cased_string:

    Returns:

    """

    camel_cased_string = snake_cased_string.replace("-", " ").\
        replace("_", " ").split()
    camel_cased_string = (
            camel_cased_string[0] +
            ''.join(i.capitalize() for i in camel_cased_string[1:])
    )
    return camel_cased_string


def from_camel_to_snake_case(camel_cased_string: str) -> str:
    """

    Args:
        camel_cased_string:

    Returns:

    """

    pattern = re.compile(r'(?<!^)(?=[A-Z])')
    snake_cased_string = pattern.sub('_', camel_cased_string).lower()
    return snake_cased_string


def from_snake_dict_keys_to_camel_case_keys(
        snake_cased_keys_dict: dict
) -> dict:
    """

    Args:
        snake_cased_keys_dict:

    Returns:

    """

    camel_cased_keys_dict = {
        from_snake_to_camel_case(key): value
        for key, value in snake_cased_keys_dict.items()
    }
    return camel_cased_keys_dict


def clean_graphql_query_fields(
        dirty_graphql_query_fields: str
) -> typing.List[str]:
    """

    Args:
        dirty_graphql_query_fields:

    Returns:

    """
    clean_fields = re.split(r"[\W]+", dirty_graphql_query_fields)
    fields = [
        from_camel_to_snake_case(field)
        for field in clean_fields if field is not None
    ]
    return fields


def add_db_table_prefix_to_gql_query_fields(
        query_fields: list,
        db_table_prefix: str,
) -> typing.List[str]:
    """
    Adds a database table name prefix to every GrapQL query field specified.

    Args:
        query_fields:
            An array of strings, where each array element is a single GraphQL
            field.
        db_table_prefix:
            A snake-cased string.

    Returns:
        An array of strings, whose values are concatenated strings
        (db_table_prefix argument plus each query field from the query_fields
        argument.)
        For example:

        If query_fields = [my_first_field, my_second_field, my_third_field], and
        db_table_prefix = 'my_table_prefix', the return value will be

        ['my_table_prefix_my_first_field',
        'my_table_prefix_my_second_field',
        'my_table_prefix_my_third_field']
    """

    _query_fields = [
        '{}_{}'.format(db_table_prefix, query_field)
        for query_field in query_fields
    ]
    return _query_fields


def remove_db_table_prefix_from_retrieved_db_data(
        retrieved_data: typing.Union[Record, list, dict, typing.Mapping],
        db_table_prefix: str
):
    """

    Args:
        retrieved_data:
        db_table_prefix:

    Returns:

    """

    data = None
    if isinstance(retrieved_data, Record) or isinstance(retrieved_data, dict):
        data = {key.replace(db_table_prefix, ''): value
                for key, value in retrieved_data.items()}
    elif isinstance(retrieved_data, list):
        _retrieved_data = [dict(item) for item in retrieved_data]
        data = [
            remove_db_table_prefix_from_retrieved_db_data(item, db_table_prefix)
            for item in _retrieved_data
        ]
    return data
