=====
term
=====
--------------------------------------
An enhanced version of the tty module
--------------------------------------

Overview
========

The **term** package is an enhanced version of the standard library's
tty_ module.
It provides context managers for temporarily switching the terminal
to *raw* or *cbreak* mode and allows to query cursor position and terminal
dimensions without having to resort to curses.

.. _tty: http://docs.python.org/library/tty.html

Package Contents
================

setraw(fd, when=TCSAFLUSH, min=1, time=0)
    Put the terminal in raw mode.

setcbreak(fd, when=TCSAFLUSH, min=1, time=0)
    Put the terminal in cbreak mode.

rawmode(fd, when=TCSAFLUSH, min=1, time=0)
    Context manager to put the terminal in raw mode.

cbreakmode(fd, when=TCSAFLUSH, min=1, time=0)
    Context manager to put the terminal in cbreak mode.

opentty(bufsize=1)
    Context manager returning an rw stream connected to /dev/tty.
    The stream is None if the device could not be opened.

getyx()
    Return the cursor position as 1-based (row, col) tuple.
    row and col are 0 if the terminal does not support DSR 6.

getmaxyx()
    Return the terminal dimensions as (maxrow, maxcol) tuple.
    maxrow and maxcol are 0 if the terminal does not support DSR 6.

Examples
========
::

    from term import getyx

    print 'The cursor is in line %d column %d' % getyx()

You may also want to look at the `source code`_ of getyx, which is a
good example of how all this plays together.

.. _`source code`: https://github.com/stefanholek/term/blob/master/term/__init__.py#L119

