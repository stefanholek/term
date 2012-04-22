
def b(string, encoding='ascii'):
    """Used instead of b'' literals to stay Python 2.5 compatible.

    'encoding' should match the encoding of the source file.
    """
    if isinstance(string, unicode):
        return string.encode(encoding)
    return string
