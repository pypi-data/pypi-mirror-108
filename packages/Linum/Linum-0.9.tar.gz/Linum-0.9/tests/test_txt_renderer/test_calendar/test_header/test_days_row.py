from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.header.day.day_cell import DayCell
from linum.txt_renderer.calendar.header.day.days_row import DaysRow


class TestDaysRow(TestCase):

    def test_cells(self):
        # Перед границей месяца
        cell_width = 3
        dr = DaysRow(date(2020, 1, 30), 2)
        dr.cell_width = cell_width
        d1 = DayCell(cell_width, date(2020, 1, 30))
        d2 = DayCell(cell_width, date(2020, 1, 31))
        self.assertEqual([d1, d2], dr.cells)

        # На границе месяца c границами между месяцами
        cell_width = 3
        dr = DaysRow(date(2020, 1, 31), 2)
        dr.cell_width = cell_width
        dr.month_inner_borders = True
        d1 = DayCell(cell_width, date(2020, 1, 31))
        d1.right_border = True
        d2 = DayCell(cell_width, date(2020, 2, 1))
        d2.left_border = True
        d2.left_border = True
        cells = dr.cells
        self.assertEqual([d1, d2], dr.cells)

        # На границе месяца без границ между месяцами
        cell_width = 3
        dr = DaysRow(date(2020, 1, 31), 2)
        dr.cell_width = cell_width
        d1 = DayCell(cell_width, date(2020, 1, 31))
        d2 = DayCell(cell_width, date(2020, 2, 1))
        self.assertEqual([d1, d2], dr.cells)

        # После границы месяца
        cell_width = 3
        dr = DaysRow(date(2020, 2, 1), 2)
        dr.cell_width = cell_width
        d1 = DayCell(cell_width, date(2020, 2, 1))
        d2 = DayCell(cell_width, date(2020, 2, 2))
        self.assertEqual([d1, d2], dr.cells)

    def test_render(self):
        # Перед границей месяца
        cell_width = 3
        dr = DaysRow(date(2020, 1, 30), 2)
        dr.cell_width = cell_width
        self.assertEqual("30 31 ", dr.render())

        # На границе месяца c границами между месяцами
        cell_width = 3
        dr = DaysRow(date(2020, 1, 31), 2)
        dr.cell_width = cell_width
        dr.month_inner_borders = True
        self.assertEqual("31 │ 1 ", dr.render())

        # На границе месяца без границ между месяцами
        cell_width = 3
        dr = DaysRow(date(2020, 1, 31), 2)
        dr.cell_width = cell_width
        self.assertEqual("31  1 ", dr.render())

        # После границы месяца
        cell_width = 3
        dr = DaysRow(date(2020, 2, 1), 2)
        dr.cell_width = cell_width
        self.assertEqual(" 1  2 ", dr.render())

