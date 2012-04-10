import sys
import unittest

from termios import *
from term import *


class TermTests(unittest.TestCase):

    def setUp(self):
        self.saved = tcgetattr(sys.stdin)

    def tearDown(self):
        tcsetattr(sys.stdin, TCSAFLUSH, self.saved)

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
        self.assertRaises(TypeError, setraw, None)
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(TermIOSError, setraw, stdin)

    def test_setcbreak_raises_on_bad_fd(self):
        self.assertRaises(TypeError, setcbreak, None)
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(TermIOSError, setcbreak, stdin)

    def test_rawmode_raises_on_bad_fd(self):
        self.assertRaises(TypeError, rawmode(None).__enter__)
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(TermIOSError, rawmode(stdin).__enter__)

    def test_cbreakmode_raises_on_bad_fd(self):
        self.assertRaises(TypeError, cbreakmode(None).__enter__)
        with open('/dev/null', 'w+') as stdin:
            self.assertRaises(TermIOSError, cbreakmode(stdin).__enter__)

    def test_opentty(self):
        with opentty() as tty:
            self.assertNotEqual(tty, None)
            self.assertEqual(tty.mode, 'w+')

    def test_getyx(self):
        row, col = getyx()
        self.assertNotEqual(row, 0)
        self.assertNotEqual(col, 0)

    def test_getmaxyx(self):
        maxrow, maxcol = getmaxyx()
        self.assertNotEqual(maxrow, 0)
        self.assertNotEqual(maxcol, 0)

