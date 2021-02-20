from ariadne import ObjectType
import sqlalchemy

from ...database.crud import ArtistProfileInformationDB, StoryDB

from .utils import (
    from_snake_dict_keys_to_camel_case_keys,
    add_db_table_prefix_to_gql_query_fields,
    remove_db_table_prefix_from_retrieved_db_data
)


artist = ObjectType('Artist')


@artist.field('profileInfo')
async def resolve_profile_info(obj, info, *_):
    """

    Args:
        obj:
        info:
        *_:

    Returns:

    """

    profile_info_fields = info.context['subqueries']['profile_info']

    _db = ArtistProfileInformationDB()
    q_fields_with_prefix = add_db_table_prefix_to_gql_query_fields(profile_info_fields, _db.attribute_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    artist_id = obj['id']
    where_clause = sqlalchemy.and_(_db.table.c.artist_id_fk == artist_id)
    profile_info = await _db.fetch_one(cols, where_clause)
    if profile_info:
        _profile_info = remove_db_table_prefix_from_retrieved_db_data(profile_info, _db.attribute_prefix)
        artist_profile_info = from_snake_dict_keys_to_camel_case_keys(_profile_info)
        return artist_profile_info


@artist.field('stories')
async def resolve_stories(obj, info, *_):
    """

    Args:
        obj:
        info:
        *_:

    Returns:

    """

    stories_fields = info.context['subqueries']['stories']

    _db = StoryDB()
    q_fields_with_prefix = add_db_table_prefix_to_gql_query_fields(stories_fields, _db.attribute_prefix)
    cols = [sqlalchemy.Column(field) for field in q_fields_with_prefix]
    artist_id = obj['id']
    where_clause_val = {'artist_id': artist_id}
    artist_stories = await _db.fetch_artist_stories(cols, where_clause_val)
    _stories = remove_db_table_prefix_from_retrieved_db_data(artist_stories, _db.attribute_prefix)
    stories = [from_snake_dict_keys_to_camel_case_keys(story) for story in _stories]
    return stories
