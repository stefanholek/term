# python -m term

from __future__ import print_function

import term


if __name__ == '__main__':
    print('term.getyx', term.getyx())
    print('term.getyx_stdin_stdout', term.getyx_stdin_stdout())
    print('term.getfgcolor', term.getfgcolor())
    print('term.getbgcolor', term.getbgcolor())
    print('term.getnumcolors', term.getnumcolors())
    print('term.name', term.name())
    print('term.isxterm', term.isxterm())
    print('term.islightmode', term.islightmode())
    print('term.isdarkmode', term.isdarkmode())

