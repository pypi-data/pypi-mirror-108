from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.header.weekday.weekday_cell import WeekdayCell


class TestWeekday(TestCase):

    def test_pre_render(self):
        # Пререндер пустой ячейки
        d = WeekdayCell()
        self.assertEqual('', d.pre_render())

        # Пререндер ячейки с отрицательной длиной
        d = WeekdayCell()
        d.cell_width = -10
        self.assertEqual('', d.pre_render())

        # Пререндер обычной ячейки
        d = WeekdayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        self.assertEqual('Wed', d.pre_render())

    def test_render(self):
        # Рендер пустой ячейки
        d = WeekdayCell()
        self.assertEqual('', d.render())

        # Рендер ячейки с отрицательной длиной
        d = WeekdayCell()
        d.cell_width = -10
        self.assertEqual('', d.render())

        # Рендер обычной ячейки
        d = WeekdayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        self.assertEqual('Wed', d.render())

        # Рендер ячейки с левой границей
        d = WeekdayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        d.left_border = True
        self.assertEqual('│Wed', d.render())

        # Рендер ячейки с правой границей
        d = WeekdayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        d.right_border = True
        self.assertEqual('Wed│', d.render())

        # Рендер ячейки с двумя границами
        d = WeekdayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        d.left_border = True
        d.right_border = True
        self.assertEqual('│Wed│', d.render())

        # Рендер ячейки нулевой длины с двумя границами
        d = WeekdayCell(date_=date(2020, 1, 1))
        d.cell_width = 0
        d.left_border = True
        d.right_border = True
        self.assertEqual('││', d.render())
