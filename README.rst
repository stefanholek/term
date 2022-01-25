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

opentty(bufsize=-1)
    Context manager returning an rw stream connected to /dev/tty.
    The stream is None if the device cannot be opened.

readto(fd, stopbyte):
    Read bytes from stream, up to and including stopbyte.

High-level Functions
--------------------

getyx()
    Return the cursor position as 1-based (line, col) tuple.
    Line and col are 0 if the device cannot be opened or the terminal
    does not support DSR 6.

isxterm()
    Return true if the TERM environment variable starts with 'xterm-'.

islightmode()
    Return true if the background color is lighter than the foreground color.
    May return None if the terminal does not support OSC color requests.

isdarkmode()
    Return true if the background color is darker than the foreground color.
    May return None if the terminal does not support OSC color requests.

Examples
========

To resize the terminal window, enter cbreak mode and write the new
dimensions to the tty:

.. code-block:: python

    from term import opentty, cbreakmode

    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0):
                tty.write(b'\033[8;25;80t');

            print('terminal resized')

The getyx function may be implemented like this:

.. code-block:: python

    from re import search
    from term import opentty, cbreakmode, readto

    def getyx():
        with opentty() as tty:
            if tty is not None:
                with cbreakmode(tty, min=0, time=2):
                    tty.write(b'\033[6n')
                    p = readto(tty, b'R')
                    if p:
                        m = search(b'(\\d+);(\\d+)R$', p)
                        if m is not None:
                            return int(m.group(1)), int(m.group(2))
        return 0, 0


Documentation
=============

Please also see the `API Documentation`_.

.. _`API Documentation`: https://term.readthedocs.io/en/stable/

