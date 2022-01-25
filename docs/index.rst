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

The :mod:`term` module is an enhanced version of the :mod:`tty <py3k:tty>` module.

API Documentation
=================

Terminal Control
================

.. autofunction:: term.setraw(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.setcbreak(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.rawmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.cbreakmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.opentty
.. autofunction:: term.readto

High-level Functions
====================

.. autofunction:: term.getyx
.. autofunction:: term.isxterm
.. autofunction:: term.islightmode
.. autofunction:: term.isdarkmode

.. seealso::

   Module :mod:`termios <py3k:termios>`
      Low-level terminal control interface.

   `Xterm Control Sequences <https://invisible-island.net/xterm/ctlseqs/ctlseqs.html>`_
      Detailed list of escape sequences accepted by xterm.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

