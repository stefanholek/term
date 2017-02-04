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

The :mod:`term` module is a replacement for the :mod:`tty <py3k:tty>` module.

API Documentation
=================

.. autofunction:: term.setraw(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.setcbreak(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.rawmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.cbreakmode(fd, when=TCSAFLUSH, min=1, time=0)
.. autofunction:: term.opentty
.. autofunction:: term.getyx

.. seealso::

   Module :mod:`termios <py3k:termios>`
      Low-level terminal control interface.

   `Xterm Control Sequences <http://www.xfree86.org/4.8.0/ctlseqs.html>`_
      Detailed list of escape sequences accepted by xterm.

Indices and Tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

