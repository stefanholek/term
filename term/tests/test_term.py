import sys
import unittest
import termios

from termios import *
from term import *


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
        self.assertEqual(mode[CC][VMIN], b'\x01')
        self.assertEqual(mode[CC][VTIME], b'\x00')

    def test_setraw(self):
        setraw(sys.stdin, min=0, time=1)
        mode = tcgetattr(sys.stdin)
        self.assertEqual(mode[LFLAG] & ECHO, 0)
        self.assertEqual(mode[LFLAG] & ICANON, 0)
        self.assertEqual(mode[LFLAG] & IEXTEN, 0)
        self.assertEqual(mode[LFLAG] & ISIG, 0)
        self.assertEqual(mode[CC][VMIN], 0)
        self.assertEqual(mode[CC][VTIME], 1)

    def test_setcbreak(self):
        setcbreak(sys.stdin, min=0, time=1)
        mode = tcgetattr(sys.stdin)
        self.assertEqual(mode[LFLAG] & ECHO, 0)
        self.assertEqual(mode[LFLAG] & ICANON, 0)
        self.assertEqual(mode[LFLAG] & IEXTEN, IEXTEN)
        self.assertEqual(mode[LFLAG] & ISIG, ISIG)
        self.assertEqual(mode[CC][VMIN], 0)
        self.assertEqual(mode[CC][VTIME], 1)

    def test_rawmode(self):
        with rawmode(sys.stdin, min=0, time=1):
            mode = tcgetattr(sys.stdin)
            self.assertEqual(mode[LFLAG] & ECHO, 0)
            self.assertEqual(mode[LFLAG] & ICANON, 0)
            self.assertEqual(mode[LFLAG] & IEXTEN, 0)
            self.assertEqual(mode[LFLAG] & ISIG, 0)
            self.assertEqual(mode[CC][VMIN], 0)
            self.assertEqual(mode[CC][VTIME], 1)
        self.test_defaults()

    def test_cbreakmode(self):
        with cbreakmode(sys.stdin, min=0, time=1):
            mode = tcgetattr(sys.stdin)
            self.assertEqual(mode[LFLAG] & ECHO, 0)
            self.assertEqual(mode[LFLAG] & ICANON, 0)
            self.assertEqual(mode[LFLAG] & IEXTEN, IEXTEN)
            self.assertEqual(mode[LFLAG] & ISIG, ISIG)
            self.assertEqual(mode[CC][VMIN], 0)
            self.assertEqual(mode[CC][VTIME], 1)
        self.test_defaults()

    def test_setraw_raises_on_bad_fd(self):
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(termios.error, setraw, stdin)

    def test_setcbreak_raises_on_bad_fd(self):
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(termios.error, setcbreak, stdin)

    def test_rawmode_raises_on_bad_fd(self):
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(termios.error, rawmode(stdin).__enter__)

    def test_cbreakmode_raises_on_bad_fd(self):
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(termios.error, cbreakmode(stdin).__enter__)

    def test_setraw_raises_on_None_fd(self):
        self.assertRaises(TypeError, setraw, None)

    def test_setcbreak_raises_on_None_fd(self):
        self.assertRaises(TypeError, setcbreak, None)

    def test_rawmode_raises_on_None_fd(self):
        self.assertRaises(TypeError, rawmode(None).__enter__)

    def test_cbreakmode_raises_on_None_fd(self):
        self.assertRaises(TypeError, cbreakmode(None).__enter__)

    def test_opentty(self):
        with opentty() as tty:
            self.assertNotEqual(tty, None)
            self.assertEqual(tty.mode, 'w+')

    def test_opentty_accepts_bufsize_argument(self):
        with opentty(1) as tty:
            self.assertNotEqual(tty, None)

    def test_opentty_returns_None_on_bad_device(self):
        opener = opentty()
        opener.device = '/dev/foobar'
        with opener as tty:
            self.assertEqual(tty, None)

    def test_opentty_raises_on_None_device(self):
        self.assertRaises(TypeError, opentty(None).__enter__)

    def test_getyx(self):
        row, col = getyx()
        self.assertNotEqual(row, 0)
        self.assertNotEqual(col, 0)

    def test_getmaxyx(self):
        maxrow, maxcol = getmaxyx()
        self.assertNotEqual(maxrow, 0)
        self.assertNotEqual(maxcol, 0)

    def test_getmaxyx_restores_cursor_pos(self):
        row, col = getyx()
        maxrow, maxcol = getmaxyx()
        self.assertEqual(getyx(), (row, col))

