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


#def get_subqueries(query):
#
#    innermost_subq_pattern = re.compile(r'(\w*) ({(?:{??[^{]*?}))')
#    try:
#        get_innermost_subquery(query, innermost_subq_pattern)
#
#    return


def get_innermost_subquery(
        query: str,
        pattern: Pattern,
        subqs_found: list
) -> typing.Optional[list]:
    """

    Args:
        query:
        pattern:
        subqs_found:

    Returns:

    """

    # look for deepest subqueries according to subq pattern
    # tuple of the form ('name of subqs', 'raw attribs string')
    for match in pattern.finditer(query):
        subq = match.group(1, 2)
        subq_string = match.group()
        subqs_found.append(subq)
        query = query.replace(subq_string, '')
    if pattern.search(query):
        get_innermost_subquery(query, pattern, subqs_found)
    return subqs_found

#    if not subqs_found:
#        return None
#    else:
#        subq_names = [to_snake_case(subqs[0]) for subqs in subqs_found]
#        subq_attribs = [clean_query_attribs(subqs[1]) for subqs in subqs_found]
#        innermost_subqs = {subq_name: subq_attribs for (subq_name, subq_attribs) in zip(subq_names, subq_attribs)}
#        remaining_query = {'query': query}
#
#        #! it works but it needs recursion. query should not get out of this function
#        # until there are no other subqueries
#        return [innermost_subqs]

