=====
term
=====
--------------------------------------
An enhanced version of the tty module
--------------------------------------

Overview
========

The **term** package is an enhanced version of the standard library's
tty_ module. It provides context managers for opening a terminal stream, and
for temporarily switching the terminal to raw or cbreak mode.

.. _tty: https://docs.python.org/3/library/tty.html

Package Contents
================

Terminal Control
----------------

setraw(fd, when=TCSAFLUSH, min=1, time=0)
    Put the terminal in raw mode.

setcbreak(fd, when=TCSAFLUSH, min=1, time=0)
    Put the terminal in cbreak mode.

rawmode(fd, when=TCSAFLUSH, min=1, time=0)
    Context manager to put the terminal in raw mode.

cbreakmode(fd, when=TCSAFLUSH, min=1, time=0)
    Context manager to put the terminal in cbreak mode.

Terminal I/O
------------

opentty(bufsize=-1, mode='r+b')
    Context manager returning a new rw stream connected to /dev/tty.
    The stream is None if the device cannot be opened.

readto(stream, endswith):
    Read bytes or characters from stream until buffer.endswith(endswith)
    is true.

High-level Functions
--------------------

getyx()
    Return the cursor position as 1-based (line, col) tuple.
    Line and col are 0 if the device cannot be opened or the terminal
    does not support DSR 6.

getfgcolor()
    Return the terminal foregound color as (r, g, b) tuple.
    All values are -1 if the device cannot be opened or does not supports
    OSC 10.

getbgcolor()
    Return the terminal background color as (r, g, b) tuple.
    All values are -1 if the device cannot be opened or does not supports
    OSC 11.

islightmode()
    Return true if the background color is lighter than the foreground color.
    May return None if the terminal does not support OSC color queries.

isdarkmode()
    Return true if the background color is darker than the foreground color.
    May return None if the terminal does not support OSC color queries.

Documentation
=============

Please see the `API Documentation`_ for more.

.. _`API Documentation`: https://term.readthedocs.io/en/stable/

