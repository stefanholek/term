"""Terminal utilities."""

import sys
import re

from termios import *

__all__ = ["setraw", "setcbreak", "rawmode", "cbreakmode", "getyx", "getmaxyx",
           "IFLAG", "OFLAG", "CFLAG", "LFLAG", "ISPEED", "OSPEED", "CC"]

# Indexes for termios list.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6


def setraw(fd=None, when=TCSAFLUSH, min=1, time=0):
    """Put terminal into a raw mode."""
    fd = fd or sys.stdin
    mode = tcgetattr(fd)
    mode[IFLAG] = mode[IFLAG] & ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON)
    mode[OFLAG] = mode[OFLAG] & ~(OPOST)
    mode[CFLAG] = mode[CFLAG] & ~(CSIZE | PARENB)
    mode[CFLAG] = mode[CFLAG] | CS8
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON | IEXTEN | ISIG)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


def setcbreak(fd=None, when=TCSAFLUSH, min=1, time=0):
    """Put terminal into a cbreak mode."""
    fd = fd or sys.stdin
    mode = tcgetattr(fd)
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


class rawmode(object):
    """Context manager to put the terminal in raw mode."""

    def __init__(self, fd=None, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd or sys.stdin
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        self.saved = tcgetattr(self.fd)
        setraw(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.saved)


class cbreakmode(object):
    """Context manager to put the terminal in cbreak mode."""

    def __init__(self, fd=None, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd or sys.stdin
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        self.saved = tcgetattr(self.fd)
        setcbreak(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.saved)


def _readyx():
    """Read a CSI R formatted response from sys.stdin."""
    p = ''
    c = sys.stdin.read(1)
    while c:
        p += c
        if c == 'R':
            break
        c = sys.stdin.read(1)
    if p:
        m = re.search(r'\[(\d+);(\d+)R', p)
        if m is not None:
            return int(m.group(1), 10), int(m.group(2), 10)
    return 0, 0


def getyx():
    """Return the cursor position as 1-based (row, col) tuple.

    row and col are 0 if the terminal does not support DSR 6.
    Note that you cannot pass fds to getyx; it will always use
    sys.stdin and sys.stdout to communicate with the terminal.
    """
    with cbreakmode(min=0, time=1):
        sys.stdout.write('\033[6n')
        return _readyx()


def getmaxyx():
    """Return the terminal window dimensions as (maxrow, maxcol) tuple.

    maxrow and maxcol are 0 if the terminal does not support DSR 6.
    Note that you cannot pass fds to getmaxyx; it will always use
    sys.stdin and sys.stdout to communicate with the terminal.
    """
    with cbreakmode(min=0, time=1):
        row, col = getyx()
        try:
            sys.stdout.write('\033[10000;10000f\033[6n')
            return _readyx()
        finally:
            sys.stdout.write('\033[%d;%df' % (row, col))

