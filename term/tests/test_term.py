import sys
import os
import unittest
import termios

# pylint: disable=wildcard-import
# pylint: disable=unused-wildcard-import
from termios import *
from term import *

from term import MODE
from term import _opentty
from term import _readyx
from term import _readcolor
#from term import getyx
from term import getbgcolor
from term import getfgcolor
from term import luminance
from term import islightmode
from term import isdarkmode
from term import isxterm

if sys.version_info[0] >= 3:
    from io import BytesIO
    from io import StringIO
else:
    from StringIO import StringIO as BytesIO
    from StringIO import StringIO


# CC members VMIN and VTIME should be ints, not bytes.
# CPython and PyPy return ints in some cases and bytes in others.
def int_(x):
    if not isinstance(x, int):
        x = ord(x)
    return x


class setterm(object):
    def __init__(self, val):
        self._val = val
        self._saved = None
    def __enter__(self):
        self._saved = os.environ.get('TERM', '')
        os.environ['TERM'] = self._val
    def __exit__(self, *ignored):
        os.environ['TERM'] = self._saved


class IntegerTests(unittest.TestCase):

    def test_int(self):
        self.assertEqual(int_(0), 0)
        self.assertEqual(int_(1), 1)
        self.assertEqual(int_(255), 255)
        self.assertEqual(int_(4), 4)
        self.assertEqual(int_(32767), 32767)

    def test_bytes(self):
        self.assertEqual(int_(b'\x00'), 0)
        self.assertEqual(int_(b'\x01'), 1)
        self.assertEqual(int_(b'\xff'), 255)
        self.assertEqual(int_(b'4'), 52)
        self.assertEqual(int_(b'\x34'), 52)

    def test_bytes_too_long(self):
        self.assertRaises(TypeError, int_, b'32767')


class TermTests(unittest.TestCase):
    # pylint: disable=too-many-public-methods

    def setUp(self):
        self.savedmode = tcgetattr(sys.stdin)

    def tearDown(self):
        tcsetattr(sys.stdin, TCSAFLUSH, self.savedmode)

    def test_defaults(self):
        mode = tcgetattr(sys.stdin)
        self.assertEqual(mode[LFLAG] & ECHO, ECHO)
        self.assertEqual(mode[LFLAG] & ICANON, ICANON)
        self.assertEqual(mode[LFLAG] & IEXTEN, IEXTEN)
        self.assertEqual(mode[LFLAG] & ISIG, ISIG)
        self.assertEqual(int_(mode[CC][VMIN]), 1)
        self.assertEqual(int_(mode[CC][VTIME]), 0)

    def test_setraw(self):
        setraw(sys.stdin, min=0, time=1)
        mode = tcgetattr(sys.stdin)
        self.assertEqual(mode[LFLAG] & ECHO, 0)
        self.assertEqual(mode[LFLAG] & ICANON, 0)
        self.assertEqual(mode[LFLAG] & IEXTEN, 0)
        self.assertEqual(mode[LFLAG] & ISIG, 0)
        self.assertEqual(int_(mode[CC][VMIN]), 0)
        self.assertEqual(int_(mode[CC][VTIME]), 1)

    def test_setcbreak(self):
        setcbreak(sys.stdin, min=0, time=1)
        mode = tcgetattr(sys.stdin)
        self.assertEqual(mode[LFLAG] & ECHO, 0)
        self.assertEqual(mode[LFLAG] & ICANON, 0)
        self.assertEqual(mode[LFLAG] & IEXTEN, IEXTEN)
        self.assertEqual(mode[LFLAG] & ISIG, ISIG)
        self.assertEqual(int_(mode[CC][VMIN]), 0)
        self.assertEqual(int_(mode[CC][VTIME]), 1)

    def test_rawmode(self):
        with rawmode(sys.stdin, min=0, time=1):
            mode = tcgetattr(sys.stdin)
            self.assertEqual(mode[LFLAG] & ECHO, 0)
            self.assertEqual(mode[LFLAG] & ICANON, 0)
            self.assertEqual(mode[LFLAG] & IEXTEN, 0)
            self.assertEqual(mode[LFLAG] & ISIG, 0)
            self.assertEqual(int_(mode[CC][VMIN]), 0)
            self.assertEqual(int_(mode[CC][VTIME]), 1)
        self.test_defaults()

    def test_cbreakmode(self):
        with cbreakmode(sys.stdin, min=0, time=1):
            mode = tcgetattr(sys.stdin)
            self.assertEqual(mode[LFLAG] & ECHO, 0)
            self.assertEqual(mode[LFLAG] & ICANON, 0)
            self.assertEqual(mode[LFLAG] & IEXTEN, IEXTEN)
            self.assertEqual(mode[LFLAG] & ISIG, ISIG)
            self.assertEqual(int_(mode[CC][VMIN]), 0)
            self.assertEqual(int_(mode[CC][VTIME]), 1)
        self.test_defaults()

    def test_setraw_raises_on_bad_fd(self):
        with open('/dev/null', MODE) as stdin:
            self.assertRaises(termios.error, setraw, stdin)

    def test_setcbreak_raises_on_bad_fd(self):
        with open('/dev/null', MODE) as stdin:
            self.assertRaises(termios.error, setcbreak, stdin)

    def test_rawmode_raises_on_bad_fd(self):
        with open('/dev/null', MODE) as stdin:
            self.assertRaises(termios.error, rawmode(stdin).__enter__)

    def test_cbreakmode_raises_on_bad_fd(self):
        with open('/dev/null', MODE) as stdin:
            self.assertRaises(termios.error, cbreakmode(stdin).__enter__)

    def test_setraw_raises_on_None_fd(self):
        self.assertRaises(TypeError, setraw, None)

    def test_setcbreak_raises_on_None_fd(self):
        self.assertRaises(TypeError, setcbreak, None)

    def test_rawmode_raises_on_None_fd(self):
        self.assertRaises(TypeError, rawmode(None).__enter__)

    def test_cbreakmode_raises_on_None_fd(self):
        self.assertRaises(TypeError, cbreakmode(None).__enter__)

    def test__opentty(self):
        tty = _opentty('/dev/tty', -1)
        self.assertNotEqual(tty, None)
        tty.close()

    def test__opentty_unbuffered(self):
        tty = _opentty('/dev/tty', 0)
        self.assertNotEqual(tty, None)
        tty.close()

    def test__opentty_buffered(self):
        tty = _opentty('/dev/tty', 512)
        self.assertNotEqual(tty, None)
        tty.close()

    def test__opentty_line_buffered(self):
        tty = _opentty('/dev/tty', 1)
        self.assertNotEqual(tty, None)
        tty.close()

    def test_opentty(self):
        with opentty() as tty:
            self.assertNotEqual(tty, None)
            self.assertEqual(sorted(tty.mode), sorted(MODE))

    def test_opentty_accepts_bufsize_argument(self):
        with opentty(-1) as tty:
            self.assertNotEqual(tty, None)

    def test_opentty_returns_None_on_bad_device(self):
        opener = opentty()
        opener.device = '/dev/foobar'
        with opener as tty:
            self.assertEqual(tty, None)

    def test__readyx(self):
        stream = BytesIO(b'\033[24;1R')
        self.assertEqual(_readyx(stream), (24, 1))

    def test__readyx_empty(self):
        stream = BytesIO()
        self.assertEqual(_readyx(stream), (0, 0))

    def test__readyx_too_short(self):
        stream = BytesIO(b'\033[24;1')
        self.assertEqual(_readyx(stream), (0, 0))

    def test__readyx_not_a_number(self):
        stream = BytesIO(b'\033[24;%R')
        self.assertEqual(_readyx(stream), (0, 0))

    def test_getyx(self):
        line, col = getyx()
        self.assertNotEqual(line, 0)
        self.assertNotEqual(col, 0)

    def test_readto_3(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, b'3'), b'123')

    def test_readto_7(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, b'7'), b'1234567')

    def test_readto_4_or_5(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, (b'5', b'4')), b'1234')

    def test_readto_456(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, b'456'), b'123456')

    def test_readto_end_if_bad_stopbyte(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, b'0'), b'123456789')

    def test_readto_end_if_empty_stopbyte(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, b''), b'123456789')

    def test_readto_end_if_empty_stopbyte_in_tuple(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, (b'',)), b'123456789')

    def test_readto_end_if_empty_tuple(self):
        stream = BytesIO(b'123456789')
        self.assertEqual(readto(stream, ()), b'123456789')

    def test_readto_empty_stream(self):
        stream = BytesIO(b'')
        self.assertEqual(readto(stream, b'3'), b'')

    def test_stringio_readto_3(self):
        stream = StringIO('123456789')
        self.assertEqual(readto(stream, '3'), '123')

    def test_stringio_readto_4_or_5(self):
        stream = StringIO('123456789')
        self.assertEqual(readto(stream, ('5', '4')), '1234')

    def test_stringio_readto_456(self):
        stream = StringIO('123456789')
        self.assertEqual(readto(stream, '456'), '123456')

    def test_stringio_readto_end_if_empty_stopchar(self):
        stream = StringIO('123456789')
        self.assertEqual(readto(stream, ''), '123456789')

    def test_stringio_readto_end_if_empty_stopchar_in_tuple(self):
        stream = StringIO('123456789')
        self.assertEqual(readto(stream, ('',)), '123456789')

    def test_stringio_readto_end_if_empty_tuple(self):
        stream = StringIO('123456789')
        self.assertEqual(readto(stream, ()), '123456789')

    def test_stringio_readto_empty_stream(self):
        stream = StringIO('')
        self.assertEqual(readto(stream, '3'), '')

    def test__readcolor(self):
        stream = BytesIO(b'\033]10;rgb:00ff/ff00/0ff0\007')
        self.assertEqual(_readcolor(stream), (255, 65280, 4080))

    def test__readcolor_empty(self):
        stream = BytesIO()
        self.assertEqual(_readcolor(stream), (-1, -1, -1))

    def test__readcolor_too_short(self):
        stream = BytesIO(b'\033]10;rgb:00ff/ff00/0ff0')
        self.assertEqual(_readcolor(stream), (-1, -1, -1))

    def test__readcolor_not_a_hex_number(self):
        stream = BytesIO(b'\033]10;rgb:00ff/ff00/0gg0\007')
        self.assertEqual(_readcolor(stream), (-1, -1, -1))

    def test_luminance_black(self):
        self.assertEqual(luminance((0, 0, 0)), 0)

    def test_luminance_white(self):
        self.assertAlmostEqual(luminance((65535, 65535, 65535)), 65535)

    def test_luminance_oceanblue(self):
        self.assertAlmostEqual(luminance((11103, 26278, 51575)), 27302.756912974924)

    def test_luminance_sandred(self):
        self.assertAlmostEqual(luminance((36524, 13538, 10094)), 22761.062302889117)

    def test_getbgcolor(self):
        rgb = getbgcolor()
        self.assertNotEqual(rgb, (-1, -1, -1))

    def test_getfgcolor(self):
        rgb = getfgcolor()
        self.assertNotEqual(rgb, (-1, -1, -1))

    def test_islightmode(self):
        self.assertNotEqual(islightmode(), None)

    def test_isdarkmode(self):
        self.assertNotEqual(isdarkmode(), None)

    def test_isxterm(self):
        with setterm('xterm-color'):
            self.assertEqual(isxterm(), True)
        with setterm('xterm-256color'):
            self.assertEqual(isxterm(), True)
        with setterm('xterm-'):
            self.assertEqual(isxterm(), True)
        with setterm('xterm'):
            self.assertEqual(isxterm(), True)

    def test_is_not_xterm_(self):
        with setterm('ansi'):
            self.assertEqual(isxterm(), False)
        with setterm('vt100'):
            self.assertEqual(isxterm(), False)

