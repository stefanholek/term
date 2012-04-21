"""The term module is intended to replace the tty module."""

# Authors: Steen Lumholt, Stefan H. Holek

import sys
import os
import re

from termios import *

__all__ = ["setraw", "setcbreak", "rawmode", "cbreakmode", "opentty", "getyx",
           "IFLAG", "OFLAG", "CFLAG", "LFLAG", "ISPEED", "OSPEED", "CC"]

# Indexes for termios list.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6


def setraw(fd, when=TCSAFLUSH, min=1, time=0):
    """Put the terminal in raw mode."""
    mode = tcgetattr(fd)
    mode[IFLAG] = mode[IFLAG] & ~(BRKINT | ICRNL | INPCK | ISTRIP | IXON)
    mode[OFLAG] = mode[OFLAG] & ~(OPOST)
    mode[CFLAG] = mode[CFLAG] & ~(CSIZE | PARENB)
    mode[CFLAG] = mode[CFLAG] | CS8
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON | IEXTEN | ISIG)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


def setcbreak(fd, when=TCSAFLUSH, min=1, time=0):
    """Put the terminal in cbreak mode."""
    mode = tcgetattr(fd)
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


class savemode(object):
    """Context manager to save and restore the terminal state."""

    def __init__(self, fd):
        self.fd = fd

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


class rawmode(savemode):
    """Context manager to put the terminal in raw mode."""

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        super(rawmode, self).__init__(fd)
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        super(rawmode, self).__enter__()
        setraw(self.fd, self.when, self.min, self.time)


class cbreakmode(savemode):
    """Context manager to put the terminal in cbreak mode."""

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        super(cbreakmode, self).__init__(fd)
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        super(cbreakmode, self).__enter__()
        setcbreak(self.fd, self.when, self.min, self.time)


def _opentty(device, bufsize):
    """Open a tty device for reading and writing."""
    fd = os.open(device, os.O_RDWR | os.O_NOCTTY)

    if not os.isatty(fd):
        return None

    if sys.version_info[0] >= 3:
        # Buffering requires a seekable device
        try:
            os.lseek(fd, 0, os.SEEK_CUR)
        except OSError:
            bufsize = 0
        return open(fd, 'rb+', bufsize)

    return os.fdopen(fd, 'r+', bufsize)


class opentty(object):
    """Context manager returning an rw stream connected to /dev/tty.

    The stream is None if the device could not be opened.
    """
    device = '/dev/tty'

    def __init__(self, bufsize=1):
        self.bufsize = bufsize

    def __enter__(self):
        self.tty = None
        try:
            self.tty = _opentty(self.device, self.bufsize)
        except EnvironmentError:
            pass
        return self.tty

    def __exit__(self, *ignored):
        if self.tty is not None:
            self.tty.close()


# See e.g. http://www.termsys.demon.co.uk/vtansi.htm

RESPONSE_WAIT_TIME = 30 # 3 seconds


def _readyx(stream):
    """Read a cursor position response from stream."""
    p = b''
    c = stream.read(1)
    while c:
        p += c
        if c == b'R':
            break
        c = stream.read(1)
    if p:
        m = re.search(b'\[(\d+);(\d+)R', p)
        if m is not None:
            return int(m.group(1), 10), int(m.group(2), 10)
    return 0, 0


def getyx():
    """Return the cursor position as 1-based (line, col) tuple.

    line and col are 0 if the terminal does not support DSR 6.
    """
    with opentty() as tty:
        line = col = 0
        if tty is not None:
            with cbreakmode(tty, min=0, time=RESPONSE_WAIT_TIME):
                tty.write(b'\033[6n')
                line, col = _readyx(tty)
        return line, col

