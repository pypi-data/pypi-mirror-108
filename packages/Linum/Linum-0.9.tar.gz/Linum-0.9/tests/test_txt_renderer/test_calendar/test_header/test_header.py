from datetime import date
from unittest import TestCase

from .fixtures import header
from linum.txt_renderer.calendar.header.header import Header


class TestHeader(TestCase):

    def test_render(self):
        # One day header
        h = Header(date(2020, 1, 1), 1)
        h.cell_width = 3
        self.assertEqual(header[1], h.render())

        # Two days header
        h = Header(date(2020, 1, 1), 2)
        h.cell_width = 3
        self.assertEqual(header[2], h.render())

        # Header with inner borders
        h = Header(date(2020, 1, 1), 2)
        h.cell_width = 3
        h.inner_borders = True
        self.assertEqual(header[3], h.render())

        # Header with left borders
        h = Header(date(2020, 1, 1), 2)
        h.cell_width = 3
        h.left_border = True
        self.assertEqual(header[4], h.render())

        # Header with right borders
        h = Header(date(2020, 1, 1), 2)
        h.cell_width = 3
        h.right_border = True
        self.assertEqual(header[5], h.render())

        # Header with month separating
        h = Header(date(2020, 1, 31), 2)
        h.cell_width = 3
        h.month_inner_borders = True
        self.assertEqual(header[6], h.render())

        # Header with inner borders on month limit
        h = Header(date(2020, 1, 31), 2)
        h.cell_width = 3
        h.inner_borders = True
        self.assertEqual(header[6], h.render())




