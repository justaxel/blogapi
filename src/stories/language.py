import typing

LANGS_ISO_6392 = {
            'english': 'eng',
            'spanish': 'spa',
            'galician': 'glg',
            'german': 'ger',
            'french': 'fre',
            'italian': 'ita',
            'portuguese': 'por'
}


def get_language_iso_code(language_request: str) -> typing.Tuple[str, str]:

    _language_request = language_request.lower()
    try:
        language_iso_6392_code = LANGS_ISO_6392[_language_request]
    except KeyError:
        raise KeyError("The language requested is not supported.")
    else:
        language_full = _language_request.title()
        return language_full, language_iso_6392_code
