from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.header.day.day_cell import DayCell


class TestDay(TestCase):

    def test_pre_render(self):
        # Пререндер пустой ячейки
        d = DayCell()
        self.assertEqual('', d.pre_render())

        # Пререндер ячейки с отрицательной длиной
        d = DayCell()
        d.cell_width = -10
        self.assertEqual('', d.pre_render())

        # Пререндер обычной ячейки
        d = DayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        self.assertEqual(' 1 ', d.pre_render())

    def test_render(self):
        # Рендер пустой ячейки
        d = DayCell()
        self.assertEqual('', d.render())

        # Рендер ячейки с отрицательной длиной
        d = DayCell()
        d.cell_width = -10
        self.assertEqual('', d.render())

        # Рендер обычной ячейки
        d = DayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        self.assertEqual(' 1 ', d.render())

        # Рендер ячейки с левой границей
        d = DayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        d.left_border = True
        self.assertEqual('│ 1 ', d.render())

        # Рендер ячейки с правой границей
        d = DayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        d.right_border = True
        self.assertEqual(' 1 │', d.render())

        # Рендер ячейки с двумя границами
        d = DayCell(date_=date(2020, 1, 1))
        d.cell_width = 3
        d.left_border = True
        d.right_border = True
        self.assertEqual('│ 1 │', d.render())

        # Рендер ячейки нулевой длины с двумя границами
        d = DayCell(date_=date(2020, 1, 1))
        d.cell_width = 0
        d.left_border = True
        d.right_border = True
        self.assertEqual('││', d.render())
