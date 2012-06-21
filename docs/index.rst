.. term documentation master file, created by
   sphinx-quickstart on Thu May 10 17:11:01 2012.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

===============================================
term |version| -- Terminal Control
===============================================

.. toctree::
   :maxdepth: 2

.. module:: term

The :mod:`term` module is intended to replace the :mod:`tty <py:tty>` module.

API Documentation
=================

.. autofunction:: term.setraw(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.setcbreak(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.rawmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.cbreakmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.opentty
.. autofunction:: term.getyx

.. seealso::

   Module :mod:`termios <py:termios>`
      Low-level terminal control interface.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

