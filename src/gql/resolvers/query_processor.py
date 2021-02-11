import typing
import re
from re import Pattern

from .utils import clean_query_attribs, to_snake_case
from .custom_errors import NoRootQueryNameForGraphQLQueryWithNoArgs


def retrieve_graphql_query(query: str, has_args: bool = False) -> str:
    """

    Args:
        query:
        has_args:

    Returns:

    """

    pattern_query_no_args = re.compile(r"(\w*) {\n")

    if has_args:
        # in case the query has arguments, there is no need to manually remove
        # the root query name.
        lookup_result = re.search(r'(\w*)\"\) {\n', query)
    else:
        try:
            _query = remove_root_name_from_unarged_query(query)
            print(_query)
        except AttributeError:
            raise AttributeError(
                'Could not remove root name from unargumented graphql query.'
            )
        else:
            query = _query
        lookup_result = pattern_query_no_args.search(query)
        print(lookup_result)
    try:
        lookup_index = lookup_result.span()[1]
        print(lookup_index)
    except AttributeError:
        raise AttributeError('The query lookup returned no value.')
    else:
        query = query[lookup_index:]
        return query


def remove_root_name_from_unarged_query(query) -> str:
    """

    Args:
        query:

    Returns:

    """
    root_type_lookup = re.search(r"query (\w*) {\n", query, re.IGNORECASE)
    if not root_type_lookup:
        root_type_lookup = re.search(r"query {\n", query, re.IGNORECASE)
    query = query[root_type_lookup.span()[1]:]
    return query


def get_subqueries(query):

    subq_pattern = re.compile(r'(\w*) ({(?:{??[^{]*?}))')
    pass


def get_innermost_subquery(query, innermost_subq_pattern: Pattern):
    """

    Args:
        query:
        innermost_subq_pattern:

    Returns:

    """

    # look for deepest subquery according to subq pattern
    innermost_subq_lookup = innermost_subq_pattern.search(query)
    try:
        subq_found = innermost_subq_lookup.group()
    except AttributeError:
        raise AttributeError('No subquery found with current regular expression pattern.')
    else:
        # look for the name of found subquery
        subq_name_lookup = re.search(r'(\w*) {\n', subq_found)

    # clean subquery name from braces and spaces
    camel_subq_name = subq_name_lookup.group().replace('{', '').strip()
    # get rid of subquery name and keep only dirty subquery attributes
    dirty_subq_attribs = subq_found.replace(subq_name_lookup.group(), '')

    # clean all resources
    subq_name = to_snake_case(camel_subq_name)
    subq_attribs = clean_query_attribs(dirty_subq_attribs)
    return {subq_name: subq_attribs}

