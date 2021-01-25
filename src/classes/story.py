import secrets

from ..database.crud import StoryDB

class Story:
    
    def __init__(
        self,
        author: str,
        title: str,
        content: str = None,
        synopsis: str = None,
        language_iso_6392: str = None,
        is_published: bool = False,
        is_test: bool = False
    ) -> None:

        self.author = author
        if title:
            self.title = title.encode('utf-8')
        if content:
            self.content = content.encode('utf-8')
        if synopsis:
            self.synopsis = synopsis.encode('utf-8')
        self.language = language_iso_6392
        self.is_published = is_published
        self._db = StoryDB(is_test)
    
    def set_content(self, content: str) -> bytes:

        self.content = content.encode('utf-8')
        return self.content
    
    def set_synopsis(self, content: str) -> bytes:

        self.content = content.encode('utf-8')
        return self.content
    
    def set_language(self, language: str) -> str:
        
        language_code = self.get_language_iso_code(language)
        self.language = language_code
        return self.language

    def get_language_iso_code(self, language: str) -> str:

        LANG_ISO_6392_CODES = {
            'english': 'eng',
            'spanish': 'spa',
            'galician': 'glg',
            'german': 'ger',
            'french': 'fre',
            'italian': 'ita',
            'portuguese': 'por'
        }

        _language = language.lower()
        try:
            language_iso_6392_code = LANG_ISO_6392_CODES[_language]
        except Exception:
            raise Exception
        else:
            return language_iso_6392_code
