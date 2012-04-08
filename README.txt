=====
term
=====
--------------------------------------
An enhanced version of the tty module
--------------------------------------

Overview
========

The **term** package is an improved version of the standard library's
tty_ module. It provides context managers for temporarily switching the terminal
to *raw* or *cbreak* mode and allows to query the cursor position and terminal
dimensions without having to resort to curses.

.. _tty: http://docs.python.org/library/tty.html

Package Contents
================

setraw(fd=None, when=TCSAFLUSH, min=1, time=0)
    Put fd in raw mode. If fd is None it defaults to sys.stdin.

setcbreak(fd=None, when=TCSAFLUSH, min=1, time=0)
    Put fd in cbreak mode. If fd is None it defaults to sys.stdin.

rawmode(fd=None, when=TCSAFLUSH, min=1, time=0)
    Context manager to put fd in raw mode. If fd is None it defaults to sys.stdin.

cbreakmode(fd=None, when=TCSAFLUSH, min=1, time=0)
    Context manager to put fd in cbreak mode. If fd is None it defaults to sys.stdin.

getyx()
    Return cursor position as 1-based (row, col) tuple.
    row and col are 0 if the terminal does not support DSR 6.

getmaxyx()
    Return terminal dimensions as (maxrow, maxcol) tuple.
    maxrow and maxcol are 0 if the terminal does not support DSR 6.

Examples
========
::

    from term import getyx

    print 'The cursor is in row %d column %d' % getyx()
