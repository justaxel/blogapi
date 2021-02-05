import typing
import re
from graphql.type.definition import GraphQLResolveInfo

from .utils import to_snake_case, clean_query_attribs
from .custom_errors import NoQueryNameForGraphQLQueryWithNoArgs, NumberOfQueryAttributesDoNotMatch


def get_graphql_query_attribs(
        query: str,
        has_args: bool = False,
        query_name: str = None,
        only_main_attribs: bool = True,
        only_subquery_attribs: bool = False,
        subquery_name: str = None
) -> typing.Dict[str, typing.List[str]]:
    """
    Returns a dictionary with information about GraphQL's queries from a GraphQL request.

    Arguments
    ---
    :str:`query: str`

    :bool:`has_args: bool = False`

    :str:`query_name: str = None`

    Returns
    ---
    :dict:`graphql_query = {
        'main_query_fields': [list, of, fields],
        'subqueries': {
            'subquery1': [list, of, subquery1, fields],
            'subquery2': [list, of, subquery2, fields]
        }
    }`
    """

    pattern_query_with_args = re.compile(r"\) {\n")
    pattern_query_no_args = re.compile(r"(\w*) {\n")

    # perform the first cleanup.
    if has_args:
        reg_result = pattern_query_with_args.search(query)
        try:
            result_index = reg_result.span()[1]
        except AttributeError:    # no result was found
            raise AttributeError('Regex pattern lookup returned no value.')
    else:
        if not query_name:
            raise NoQueryNameForGraphQLQueryWithNoArgs(
                'Please provide the name of your GraphQL query for pattern lookup.'
            )
        # find all matches for the regex pattern (no args) and only use the last one found.
        for match in re.finditer(pattern_query_no_args, query):
            end = match.end()
            result_index = end

    _query = query[result_index:]

    # returns a tuple (raw_subquery_names, raw_subquery_fields)
    raw_subqueries = get_raw_subqueries_from_graphql_query(_query)
    try:
        if only_main_attribs and not only_subquery_attribs:
            query_attribs = {'main_request': get_main_request_attribs_from_graphql_query(raw_subqueries, _query)}
        elif only_subquery_attribs and not only_main_attribs and subquery_name:
            query_attribs = get_subquery_request_attribs(raw_subqueries, subquery_name)
    except Exception:
        raise Exception
    else:
        return query_attribs


def get_main_request_attribs_from_graphql_query(
        raw_subquery_attributes: typing.Optional[tuple],
        graphql_query: str
) -> typing.List[str]:

    try:
        raw_subquery_attributes_names = raw_subquery_attributes[0]
        raw_subquery_attributes_fields = raw_subquery_attributes[1]
    except TypeError:
        main_graphql_request = clean_query_attribs(graphql_query)
    else:  # remove all nested query requests while keeping the main request.
        for subquery_attributes_index in range(len(raw_subquery_attributes_names)):
            graphql_query = graphql_query.replace(
                raw_subquery_attributes_fields[subquery_attributes_index], ''
            ).replace(
                raw_subquery_attributes_names[subquery_attributes_index], ''
            )
        # remove any non-valid characters and get all remaining characters into a list.
        main_graphql_request = clean_query_attribs(graphql_query)
    return main_graphql_request


def get_raw_subqueries_from_graphql_query(
        query: str
) -> typing.Optional[typing.Tuple[typing.List[str], typing.List[str]]]:
    """
    Collects all GraphQL's subqueries information from a raw GraphQL's query string.

    Arguments
    ---
    :str:`query: str`

    Returns
    ---
    :tuple:`([raw_subquery_names], [raw_subquery_fields])
    """

    pattern_subquery_attribs = re.compile(r"({(?:{??[^{]*?}))")
    pattern_subquery_names = re.compile(r"(\w*) {")

    reg_res_subquery_attribs = pattern_subquery_attribs.findall(query)
    reg_res_subquery_names = pattern_subquery_names.findall(query)

    # get rid of empty elements in both lists
    raw_subquery_names = [name for name in reg_res_subquery_names if name != '']
    if not raw_subquery_names:
        return None
    else:
        raw_subquery_attribs = [attrib for attrib in reg_res_subquery_attribs if attrib != '']
    return raw_subquery_names, raw_subquery_attribs


def get_subquery_request_attribs(
        raw_subqueries: typing.Tuple[typing.List[str], typing.List[str]],
        subquery_name: str
) -> typing.Dict[str, typing.List[str]]:
    """
    Cleans data from a raw subquery tuple.

    Arguments
    ---
    :tuple:`raw_subqueries: Tuple[List[str], List[str]]`

    Returns
    ---
    :dict:`subqueries = {
        'subquery1': ['list', 'of', 'subquery1', 'fields'],
        'subquery2': ['list', 'of', 'subquery2', 'fields']
    }
    """

    raw_subquery_names = raw_subqueries[0]
    raw_subquery_attribs = raw_subqueries[1]

    if len(raw_subquery_names) != len(raw_subquery_attribs):
        raise NumberOfQueryAttributesDoNotMatch

    clean_subquery_names = [to_snake_case(name) for name in raw_subquery_names]

    # get the subquery name list index.
    for i in range(len(clean_subquery_names)):
        if clean_subquery_names[i] == subquery_name:
            subquery_index = i

    # only process the subquery requested.
    req_subquery_name = clean_subquery_names[subquery_index]
    req_subquery_attribs = raw_subquery_attribs[subquery_index]

    # clean up the requested subquery fields.
    req_subquery_attribs = re.split(r"[\W]+", req_subquery_attribs)
    req_subquery_attribs = [to_snake_case(attrib) for attrib in req_subquery_attribs if attrib != '']

    subquery = {req_subquery_name: req_subquery_attribs}
    return subquery


def add_table_prefix_to_gql_query_items(
        query: typing.Dict[str, typing.List[str]],
        query_table_prefix: str,
) -> typing.Dict[str, typing.List[str]]:
    """Adds the table name prefix to GrapQL query fields."""

    _query = query.copy()
    for query_key, query_val in _query.items():
        table_prefix = query_table_prefix
        if isinstance(query_val, list):
            _query = list(map(lambda field: table_prefix + field, query_val))
    return _query


def remove_prefix_from_single_db_data(
        data: typing.Mapping,
        prefix: str
) -> dict:
    """ . """

    data = {key.replace(prefix, ''): value for key, value in data.items()}
    return data


def remove_prefix_from_multiple_db_data(
        data: typing.Optional[list],
        prefix: str
) -> typing.List[dict]:
    """."""

    _data = [dict(data_item) for data_item in data]
    _data = [remove_prefix_from_single_db_data(item, prefix) for item in _data]
    return _data


async def get_graphql_request(info: GraphQLResolveInfo) -> str:

    raw_entire_request = await info.context['request'].json()
    graphql_request = raw_entire_request['query']
    return graphql_request
