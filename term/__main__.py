# python -m term

from __future__ import print_function

import term


if __name__ == '__main__':
    print('term.getyx', term.getyx())
    print('term.getbgcolor', term.getbgcolor())
    print('term.getfgcolor', term.getfgcolor())
    print('term.isxterm', term.isxterm())
    print('term.islightmode', term.islightmode())
    print('term.isdarkmode', term.isdarkmode())

