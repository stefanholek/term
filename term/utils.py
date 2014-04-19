import sys


def b(string, encoding='utf-8'):
    """Used instead of b'' literals to stay Python 2.5 compatible.

    'encoding' should match the encoding of the source file.
    """
    if sys.version_info[0] >= 3:
        return string.encode(encoding)
    else:
        return string
