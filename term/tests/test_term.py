import unittest

from termios import *
from term import *


class TermTests(unittest.TestCase):

    def test_getyx(self):
        row, col = getyx()
        self.assertNotEqual(row, 0)
        self.assertNotEqual(col, 0)

    def test_getmaxyx(self):
        maxrow, maxcol = getmaxyx()
        self.assertNotEqual(maxrow, 0)
        self.assertNotEqual(maxcol, 0)
