from ariadne import ObjectType
import sqlalchemy

from ...database.crud import AuthorDB
from .utils import (
    from_snake_dict_keys_to_camel_case_keys,
    add_db_table_prefix_to_gql_query_fields,
    remove_db_table_prefix_from_retrieved_db_data
)


story = ObjectType('Story')


@story.field('authors')
async def resolve_authors(obj, info, *_):
    """

    Args:
        obj:
        info:
        *_:

    Returns:

    """

    authors_fields = info.context['subqueries']['authors']

    _db = AuthorDB()
    q_fields_with_prefix = add_db_table_prefix_to_gql_query_fields(authors_fields, _db.attrib_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    story_id = obj['id']
    where_clause = {'story_id': story_id}
    story_author = await _db.fetch_story_authors(cols, where_clause)
    _author = remove_db_table_prefix_from_retrieved_db_data(story_author, _db.attrib_prefix)
    authors = [from_snake_dict_keys_to_camel_case_keys(author) for author in _author]
    return authors
