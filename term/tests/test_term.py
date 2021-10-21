import sys
import unittest
import termios

from termios import *
from term import *

from term import MODE
from term import _opentty
from term import _readyx

if sys.version_info[0] >= 3:
    from io import BytesIO
else:
    from StringIO import StringIO as BytesIO


# CC members are of type unsigned char which corresponds to bytes.
# CPython and PyPy return bytes in some cases and ints in others.
def int_(x):
    if not isinstance(x, int):
        x = ord(x)
    return x


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
            self.assertEqual(tty.mode, MODE)

    def test_opentty_accepts_bufsize_argument(self):
        with opentty(-1) as tty:
            self.assertNotEqual(tty, None)

    def test_opentty_returns_None_on_bad_device(self):
        opener = opentty()
        opener.device = '/dev/foobar'
        with opener as tty:
            self.assertEqual(tty, None)

    def test__readyx(self):
        stream = BytesIO(b'\033[24;1R');
        self.assertEqual(_readyx(stream), (24, 1))

    def test__readyx_empty(self):
        stream = BytesIO();
        self.assertEqual(_readyx(stream), (0, 0))

    def test__readyx_too_short(self):
        stream = BytesIO(b'\033[24;1');
        self.assertEqual(_readyx(stream), (0, 0))

    def test__readyx_not_a_number(self):
        stream = BytesIO(b'\033[24;%R');
        self.assertEqual(_readyx(stream), (0, 0))

    def test_getyx(self):
        line, col = getyx()
        self.assertNotEqual(line, 0)
        self.assertNotEqual(col, 0)

