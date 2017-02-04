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
to *raw* or *cbreak* mode and allows to retrieve the cursor position
without having to resort to curses.

.. _tty: https://docs.python.org/3/library/tty.html

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
    Return the cursor position as 1-based (line, col) tuple.
    Line and col are 0 if the terminal does not support DSR 6.

Examples
========

To resize the terminal window, we enter cbreak mode and write the new dimensions
to the tty::

    from term import opentty, cbreakmode

    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0):
                tty.write('\033[8;25;80t');

    print 'terminal resized'

You may also want to look at the `source code`_ of getyx().

.. _`source code`: https://github.com/stefanholek/term/blob/master/term/__init__.py#L140

Caveat
======

The terminal must be in canonical mode before any of the functions and
context managers can be used. They are not meant for switching between e.g.
raw and cbreak modes. Nesting context managers of the same type is allowed
though.

