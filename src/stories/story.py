import secrets

from ..database.crud import StoryDB
from .language import get_language_iso_code


class Story:

    def __init__(
            self,
            authors: str,
            title: str,
            language: str,
            content: str = '',
            synopsis: str = '',
            is_published: bool = False,
            is_test: bool = False,
            uri: str = ''
    ) -> None:

        self.authors = authors
        self.title = title.encode('utf-8')
        self.content = content.encode('utf-8')
        self.synopsis = synopsis.encode('utf-8')
        self.language_info = get_language_iso_code(language)
        self.is_published = is_published
        self.uri = uri
        self._db = StoryDB(is_test)
    
    def set_content(self, content: str) -> bytes:

        self.content = content.encode('utf-8')
        return self.content
    
    def set_synopsis(self, content: str) -> bytes:

        self.content = content.encode('utf-8')
        return self.content
    
    def set_uri(self, safe_title: str, length: int) -> str:

        random_hash = secrets.token_hex(nbytes=length)
        self.uri = random_hash
        if safe_title:
            self.uri = safe_title + random_hash
        return self.uri

    def spew_out_data(self):
        
        story_data = {
            'authors': self.authors,
            'title': self.title,
            'content': self.content,
            'synopsis': self.synopsis,
            'language_iso_6392_code': self.language_info[1],
            'is_published': self.is_published,
            'uri': self.uri
        }
        return story_data
