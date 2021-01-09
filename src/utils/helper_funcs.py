def to_camel_case(string: str) -> str:
    
    if len(string) == 0:
        return string
    else:
        _string = string.replace("-", " ").replace("_", " ").split()
        _string = _string[0] + ''.join(i.capitalize() for i in _string[1:])
        return _string