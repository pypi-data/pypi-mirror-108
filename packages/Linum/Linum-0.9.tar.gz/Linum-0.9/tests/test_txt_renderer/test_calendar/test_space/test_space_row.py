from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.space.space_row import SpaceRow


class TestRender(TestCase):

    def test_date_cell_class(self):
        # Пустое пространство перед окончанием месяца
        sr = SpaceRow(date(2020, 1, 30), 2)
        sr.cell_width = 3
        self.assertEqual('      ', sr.render())

        # Пустое пространство перед окончанием месяца с внутренними границами
        sr = SpaceRow(date(2020, 1, 30), 2)
        sr.inner_borders = True
        sr.cell_width = 3
        self.assertEqual('   │   ', sr.render())

        # Пустое пространство на границе месяца
        sr = SpaceRow(date(2020, 1, 30), 4)
        sr.cell_width = 3
        self.assertEqual('            ', sr.render())

        # Пустое пространство на границе месяца с внутренними границами
        sr = SpaceRow(date(2020, 1, 30), 4)
        sr.cell_width = 3
        sr.inner_borders = True
        self.assertEqual('   │   │   │   ', sr.render())

        # Пустое пространство на границе месяца с границей между месяцами
        sr = SpaceRow(date(2020, 1, 30), 4)
        sr.cell_width = 3
        sr.month_inner_borders = True
        self.assertEqual('      │      ', sr.render())

