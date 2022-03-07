"""The term module is intended to replace the tty module."""

# Authors: Steen Lumholt, Stefan H. Holek

import sys
import os
import re

from math import sqrt
from termios import *

__all__ = ["setraw", "setcbreak", "rawmode", "cbreakmode",
           "IFLAG", "OFLAG", "CFLAG", "LFLAG", "ISPEED", "OSPEED", "CC",
           "opentty", "readto", "TIMEOUT",
           "getyx"] # BBB

# Indexes for termios list.
IFLAG = 0
OFLAG = 1
CFLAG = 2
LFLAG = 3
ISPEED = 4
OSPEED = 5
CC = 6

# Open /dev/tty in binary mode by default.
MODE = 'r+b'

# Wait up to 0.2 seconds for a response.
TIMEOUT = 2


def setraw(fd, when=TCSAFLUSH, min=1, time=0):
    """Put the terminal in raw mode.

    Wait until at least `min` bytes or characters have been read.
    If `min` is 0, give up after `time` (in 1/10ths of a second)
    without data becoming available.
    """
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
    """Put the terminal in cbreak mode.

    Wait until at least `min` bytes or characters have been read.
    If `min` is 0, give up after `time` (in 1/10ths of a second)
    without data becoming available.
    """
    mode = tcgetattr(fd)
    mode[LFLAG] = mode[LFLAG] & ~(ECHO | ICANON)
    mode[CC][VMIN] = min
    mode[CC][VTIME] = time
    tcsetattr(fd, when, mode)


class rawmode(object):
    """Context manager to put the terminal in raw mode.

    The current mode is saved and restored on exit.
    """

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd
        self.when = when
        self.min = min
        self.time = time
        self.savedmode = None

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)
        setraw(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


class cbreakmode(object):
    """Context manager to put the terminal in cbreak mode.

    The current mode is saved and restored on exit.
    """

    def __init__(self, fd, when=TCSAFLUSH, min=1, time=0):
        self.fd = fd
        self.when = when
        self.min = min
        self.time = time
        self.savedmode = None

    def __enter__(self):
        self.savedmode = tcgetattr(self.fd)
        setcbreak(self.fd, self.when, self.min, self.time)

    def __exit__(self, *ignored):
        tcsetattr(self.fd, TCSAFLUSH, self.savedmode)


def _opentty(device, bufsize, mode=MODE):
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
        return open(fd, mode, bufsize)
    else:
        return os.fdopen(fd, mode, bufsize)


class opentty(object):
    """Context manager returning a new rw stream connected to /dev/tty.

    The stream is None if the device cannot be opened.
    The `mode` argument must be 'r+b' (default) or 'r+'.
    """
    device = '/dev/tty'

    def __init__(self, bufsize=-1, mode=MODE):
        self.bufsize = bufsize
        self.mode = mode
        self.tty = None

    def __enter__(self):
        self.tty = None
        try:
            self.tty = _opentty(self.device, self.bufsize, self.mode)
        except EnvironmentError:
            pass
        return self.tty

    def __exit__(self, *ignored):
        if self.tty is not None:
            self.tty.close()


def _readto(stream, stopbyte):
    """Read bytes from stream, up to and including stopbyte.

    Returns an empty bytes object on EOF.
    """
    p = b''
    c = stream.read(1)
    while c:
        p += c
        if c == stopbyte:
            break
        c = stream.read(1)
    return p


def readto(stream, endswith):
    """Read bytes or characters from `stream` until buffer.endswith(`endswith`)
    is true.

    The `endswith` argument may be a single suffix or a tuple of
    suffixes to try.
    Suffixes must be bytes or str depending on the stream.
    Empty suffixes are ignored.
    """
    if not isinstance(endswith, (tuple, list)):
        endswith = (endswith,)

    c = stream.read(1)
    if isinstance(c, str):
        p = ''
        endswith = tuple(x for x in endswith if not isinstance(x, str) or x)
    else:
        p = b''
        endswith = tuple(x for x in endswith if not isinstance(x, bytes) or x)

    while c:
        p += c
        if p.endswith(endswith):
            break
        c = stream.read(1)
    return p


# linecol: printf '\033[6n' -> b'\x1b[24;1R'

def _readyx(stream):
    """Read a CPR response from stream."""
    p = readto(stream, b'R')
    if p:
        m = re.search(b'(\\d+);(\\d+)R$', p)
        if m is not None:
            return int(m.group(1), 10), int(m.group(2), 10)
    return 0, 0


def getyx():
    """Return the cursor position as 1-based (line, col) tuple.

    Line and col are 0 if the device cannot be opened or
    does not support DSR 6.
    """
    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write(b'\033[6n')
                return _readyx(tty)
    return 0, 0


def getyx_text_mode():
    """Return the cursor position as 1-based (line, col) tuple.

    Line and col are 0 if the terminal does not support
    DSR 6.
    """
    with opentty(mode='r+') as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write('\033[6n')
                tty.flush()
                p = readto(tty, 'R')
                if p:
                    m = re.search(r'(\d+);(\d+)R$', p)
                    if m is not None:
                        return int(m.group(1)), int(m.group(2))
    return 0, 0


def getyx_stdin_stdout():
    """Return the cursor position as 1-based (line, col) tuple.

    Line and col are 0 if the terminal does not support
    DSR 6.
    """
    if sys.stdin.isatty() and sys.stdout.isatty():
        with cbreakmode(sys.stdin, min=0, time=TIMEOUT):
            sys.stdout.write('\033[6n')
            sys.stdout.flush()
            p = readto(sys.stdin, 'R')
            if p:
                m = re.search(r'(\d+);(\d+)R$', p)
                if m is not None:
                    return int(m.group(1)), int(m.group(2))
    return 0, 0


# fgcolor: printf '\033]10;?\007' -> b'\x1b]10;rgb:0000/0000/0000\x07'
# bgcolor: printf '\033]11;?\007' -> b'\x1b]11;rgb:ffff/ffff/ffff\x07'

def _readcolor(stream):
    """Read an RGB color response from stream."""
    p = readto(stream, b'\007')
    if p:
        m = re.search(b'rgb:([0-9a-fA-F]+)/([0-9a-fA-F]+)/([0-9a-fA-F]+)\007$', p)
        if m is not None:
            return int(m.group(1), 16), int(m.group(2), 16), int(m.group(3), 16)
    return -1, -1, -1


def getfgcolor():
    """Return the terminal foreground color as (r, g, b) tuple.

    All values are -1 if the device cannot be opened or does not
    support OSC 10.
    """
    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write(b'\033]10;?\007')
                return _readcolor(tty)
    return -1, -1, -1


def getbgcolor():
    """Return the terminal background color as (r, g, b) tuple.

    All values are -1 if the device cannot be opened or does not
    support OSC 11.
    """
    with opentty() as tty:
        if tty is not None:
            with cbreakmode(tty, min=0, time=TIMEOUT):
                tty.write(b'\033]11;?\007')
                return _readcolor(tty)
    return -1, -1, -1


def name():
    """Return the TERM environment variable."""
    return os.environ.get('TERM', '')


def isxterm():
    """Return true if the TERM environment variable starts with 'xterm'."""
    return name().startswith('xterm')


def luminance(rgb):
    """Compute perceived brightness of RGB color tuple."""
    # https://alienryderflex.com/hsp.html
    return sqrt(0.299*rgb[0]**2 + 0.587*rgb[1]**2 + 0.114*rgb[2]**2)


def islightmode():
    """Return true if the background color is lighter than the foreground color.

    May return None if the device cannot be opened or
    does not support OSC 10 & 11.
    """
    bgcolor = getbgcolor()
    if bgcolor[0] >= 0:
        fgcolor = getfgcolor()
        if fgcolor[0] >= 0:
            return luminance(bgcolor) > luminance(fgcolor)


def isdarkmode():
    """Return true if the background color is darker than the foreground color.

    May return None if the device cannot be opened or
    does not support OSC 10 & 11.
    """
    bgcolor = getbgcolor()
    if bgcolor[0] >= 0:
        fgcolor = getfgcolor()
        if fgcolor[0] >= 0:
            return luminance(bgcolor) < luminance(fgcolor)


def getnumcolors():
    """Return the number of colors supported by the terminal.

    The result is 0 if the device cannot be opened
    or has no color support.
    """
    # pylint: disable=import-outside-toplevel
    import curses

    with opentty() as tty:
        if tty is not None:
            try:
                curses.setupterm(name(), tty.fileno())
                colors = curses.tigetnum('colors')
                if colors >= 0:
                    return colors
            except curses.error:
                pass
    return 0


def iscolor():
    """Return true if the terminal has color support."""
    return getnumcolors() > 0


def is256color():
    """Return true if the terminal has >= 256 color support."""
    return getnumcolors() >= 256


# Help autosphinx's autoattribute find the constants...
class term:
    # pylint: disable=too-few-public-methods
    IFLAG = IFLAG
    OFLAG = OFLAG
    CFLAG = CFLAG
    LFLAG = LFLAG
    ISPEED = ISPEED
    OSPEED = OSPEED
    CC = CC
    MODE = MODE
    TIMEOUT = TIMEOUT

