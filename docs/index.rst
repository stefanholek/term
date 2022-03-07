.. term documentation master file, created by
   sphinx-quickstart on Thu May 10 17:11:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================================
term |version| -- Terminal Utilities
===============================================

.. toctree::
   :maxdepth: 2

.. module:: term

The :mod:`term` module is an enhanced version of the standard library's
:mod:`tty <py3k:tty>` module.
It provides a set of functions and context managers for POSIX-style terminal
programming.

.. seealso::

    Module :mod:`termios <py3k:termios>`
        Low-level terminal control interface.

    `Xterm Control Sequences <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>`_
        Detailed list of escape sequences accepted by xterm.

API Documentation
=================

Constants
=========

.. autoattribute:: term.IFLAG

    Input modes.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.OFLAG

    Output modes.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.CFLAG

    Control modes.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.LFLAG

    Local modes.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.ISPEED

    Input speed.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.OSPEED

    Output speed.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.CC

    Control characters.
    Index into list returned by :func:`tcgetattr
    <py3k:termios.tcgetattr>`.

.. autoattribute:: term.TIMEOUT

    The default read timeout in 1/10ths of a second.

Terminal Control
================

.. autofunction:: term.setraw(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.setcbreak(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.rawmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.cbreakmode(fd, when=TCSAFLUSH, min=1, time=0)

Terminal I/O
================

.. autofunction:: term.opentty
.. autofunction:: term.readto

High-level Functions
====================

These functions are implemented using the low-level facilities above and
should probably live in a different package; yet here we are.

All functions may time out if the terminal does not respond. Set
:attr:`term.TIMEOUT` to increase the timeout.

High-level functions are not included in ``from term import *``.

.. autofunction:: term.getyx
.. autofunction:: term.getfgcolor
.. autofunction:: term.getbgcolor
.. autofunction:: term.islightmode
.. autofunction:: term.isdarkmode

Examples
========

The getyx function may be implemented like this:

.. code-block:: python

    from re import search
    from term import opentty, cbreakmode, readto

    def getyx():
        with opentty() as tty:
            if tty is not None:
                with cbreakmode(tty, min=0, time=2):  # 0.2 secs
                    tty.write(b'\033[6n')  # DSR 6
                    p = readto(tty, b'R')  # expect b'\033[24;1R'
                    if p:
                        m = search(b'(\\d+);(\\d+)R$', p)
                        if m is not None:
                            return int(m.group(1)), int(m.group(2))
        return 0, 0

Or with stdin/stdout and text I/O:

.. code-block:: python

    import sys

    from re import search
    from term import cbreakmode, readto

    def getyx():
        with cbreakmode(sys.stdin, min=0, time=2):  # 0.2 secs
            sys.stdout.write('\033[6n')
            sys.stdout.flush()
            p = readto(sys.stdin, 'R')  # expect '\033[24;1R'
            if p:
                m = search(r'(\d+);(\d+)R$', p)
                if m is not None:
                    return int(m.group(1)), int(m.group(2))
        return 0, 0

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

