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

# Open /dev/tty in binary mode.
MODE = 'rb+'

# Wait up to 3 seconds for a response.
TIMEOUT = 30


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


class rawmode(object):
    """Context manager to put the terminal in raw mode."""

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)
        setraw(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


class cbreakmode(object):
    """Context manager to put the terminal in cbreak mode."""

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd
        self.when = when
        self.min = min
        self.time = time

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)
        setcbreak(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


def _opentty(device, bufsize):
    """Open a tty device for reading and writing."""
    fd = os.open(device, os.O_RDWR | os.O_NOCTTY)

    # Line buffering is text mode only
    if bufsize == 1:
        bufsize = -1

    if sys.version_info[0] >= 3:
        # Buffering requires a seekable device
        try:
            os.lseek(fd, 0, os.SEEK_CUR)
        except OSError:
            bufsize = 0
        return open(fd, MODE, bufsize)
    else:
        return os.fdopen(fd, MODE, bufsize)


class opentty(object):
    """Context manager returning an rw stream connected to /dev/tty.

    The stream is None if the device cannot be opened.
    """
    device = '/dev/tty'

    def __init__(self, bufsize=-1):
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


def readto(stream, stopbyte):
    """Read bytes from stream, up to and including stopbyte."""
    p = b''
    c = stream.read(1)
    while c:
        p += c
        if c == stopbyte:
            break
        c = stream.read(1)
    return p


# linecol: printf '\033[6n' -> b'\x1b[24;1R'

def _readyx(stream):
    """Read a CSI R response from stream."""
    p = readto(stream, b'R')
    if p:
        m = re.search(b'(\\d+);(\\d+)R$', p)
        if m is not None:
            return int(m.group(1), 10), int(m.group(2), 10)
    return 0, 0


def getyx():
    """Return the cursor position as 1-based (line, col) tuple.

    Line and col are 0 if the device cannot be opened or the
    terminal does not support DSR 6.
    """
    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write(b'\033[6n')
                return _readyx(tty)
    return 0, 0


# bgcolor: printf '\033]11;?\007' -> b'\x1b]11;rgb:ffff/ffff/ffff\x07'
# fgcolor: printf '\033]10;?\007' -> b'\x1b]10;rgb:0000/0000/0000\x07'

def _readcolor(stream):
    """Read an RGB color response from stream."""
    p = readto(stream, b'\x07')
    if p:
        m = re.search(b'rgb:(\\w+)/(\\w+)/(\\w+)\x07$', p)
        if m is not None:
            return int(m.group(1), 16), int(m.group(2), 16), int(m.group(3), 16)
    return -1, -1, -1


def getbgcolor():
    """Return the terminal background color as (r:int, g:int, b:int) tuple.

    All values are -1 if the device cannot be opened or does not
    support the operation. Probably only works in xterm.
    """
    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write(b'\033]11;?\007')
                return _readcolor(tty)
    return -1, -1, -1


def getfgcolor():
    """Return the terminal foreground color as (r:int, g:int, b:int) tuple.

    All values are -1 if the device cannot be opened or does not
    support the operation. Probably only works in xterm.
    """
    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write(b'\033]10;?\007')
                return _readcolor(tty)
    return -1, -1, -1


def isxterm():
    """Return true if TERM environment variable starts with string 'xterm-'."""
    return os.environ.get('TERM', '').startswith('xterm-')


def luminance(rgb):
    """Compute perceived brightness of RGB color tuple."""
    return (0.2126*rgb[0] + 0.7152*rgb[1] + 0.0722*rgb[2])


def islightmode():
    """Return true if background color is lighter than foreground color.

    Returns None if the device cannot be opened or
    does not support xterm color queries.
    """
    bgcolor = getbgcolor()
    if bgcolor[0] >= 0:
        fgcolor = getfgcolor()
        if fgcolor[0] >= 0:
            return luminance(bgcolor) > luminance(fgcolor)


def isdarkmode():
    """Return true if background color is darker than foreground color.

    Returns None if the device cannot be opened or
    does not support xterm color queries.
    """
    mode = islightmode()
    if mode is not None:
        return not mode

