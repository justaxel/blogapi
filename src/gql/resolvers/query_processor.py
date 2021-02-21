"""GraphQL query processor.

This module exports the class GraphQLQueryProcessor and the necessary
function get_graphql_request(). The latter's job is to retrieve a
GraphQL query requested by a HTTP client, by using the attribute :info:
found whithin each GraphQL resolver function. The former's task is to
use this GraphQL query to find which fields are requested by using regular
expression lookup. This way, no unnecessary database fetching should be
performed.

    Usage example:

    # retrieve a graphql request
    graphql_request = get_graphql_request(info)

    # process the entire graphql query
    my_query_processor = GraphQLQueryProcessor(
        graphql_request, query_has_args=True
    )
    query_fields_found = my_query_processor.retrieve_graphql_query_fields()

    # do something to the graphql query fields
    ...
"""


import typing
import re
from graphql.type.definition import GraphQLResolveInfo

from .utils import (
    clean_graphql_query_fields,
    from_camel_to_snake_case
)


async def get_graphql_request(info: GraphQLResolveInfo) -> str:

    raw_entire_request = await info.context['request'].json()
    graphql_request = raw_entire_request['query']
    return graphql_request


class GraphQLQueryProcessor:

    def __init__(self, graphql_query, query_has_args: bool = False) -> None:
        self.query = graphql_query
        self.query_has_args = query_has_args
        self.re_innermost_subquery_pattern = re.compile(
            r'(\w*) ({(?:{??[^{]*?}))'
        )

    def retrieve_query_fields(self) -> dict:
        """

        Returns:

        """

        query = self.query
        if self.query_has_args:
            # in case the query has arguments, there is no need to
            # manually remove the root query name.
            root_query_name_lookup = re.search(r'(\w*)\"\) {\n', query)
        else:
            query = self.remove_root_name_from_unarged_query(query)
            root_query_name_lookup = re.search(r'(\w*) {\n', query)
        lookup_result_index = root_query_name_lookup.span()[1]
        query = query[lookup_result_index:]

        query_fields = self.get_graphql_query_fields(query)
        return query_fields

    @staticmethod
    def remove_root_name_from_unarged_query(query: str):
        """

        Args:
            query:

        Returns:

        """

        root_query_type_lookup = re.search(
            r'query (\w*) {\n', query, re.IGNORECASE
        )
        if not root_query_type_lookup:
            root_query_type_lookup = re.search(
                r'query {\n', query, re.IGNORECASE
            )
        query = query[root_query_type_lookup.span()[1]:]
        return query

    def get_graphql_query_fields(self, query) -> dict:
        """

        Args:
            query:

        Returns:

        """

        query_data = self.get_graphql_query_data(query)
        subqueries_found = query_data[0]
        root_query_fields = query_data[1]
        subq_names = [
            from_camel_to_snake_case(subquery_name[0])
            for subquery_name in subqueries_found
        ]
        subq_fields = [
            clean_graphql_query_fields(subquery_fields[1])
            for subquery_fields in subqueries_found
        ]
        subqueries = {
            'subqueries': {
                subq_name:
                    subq_fields
                    for (subq_name, subq_fields) in zip(subq_names, subq_fields)
            }
        }
        root_query_fields = {
            'root_query_fields': clean_graphql_query_fields(root_query_fields)
        }
        return {**root_query_fields, **subqueries}

    def get_graphql_query_data(
            self,
            query: str
    ) -> typing.Optional[typing.Tuple[list, str]]:
        """

        Args:
            query:

        Returns:

        """

        subqueries_found = []
        # look for deepest subqueries according to subq pattern
        for match in self.re_innermost_subquery_pattern.finditer(query):
            # get a tuple of the form ('name of subqs', 'raw attribs string')
            subq = match.group(1, 2)
            # get the raw string found
            subq_raw_str = match.group()
            subqueries_found.append(subq)
            query = query.replace(subq_raw_str, '')
        if self.re_innermost_subquery_pattern.search(query):
            # update the query string
            query_data = self.get_graphql_query_data(query)
            for subquery_data in query_data[0]:
                subqueries_found.append(subquery_data)
            query = query_data[1]
        return subqueries_found, query
