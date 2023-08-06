from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.header.month.month_cell import MonthCell


class TestMonthCell(TestCase):

    def test_pre_render(self):
        # Обычный пререндер
        mc = MonthCell(date_=date(2020, 1, 1))
        mc.cell_width = 11
        self.assertEqual('January `20', mc.pre_render())

        # Пререндер с центрированием
        mc = MonthCell(date_=date(2020, 1, 1))
        mc.cell_width = 13
        self.assertEqual(' January `20 ', mc.pre_render())

        # Пререндер с обрезанным содержимым
        mc = MonthCell(date_=date(2020, 1, 1))
        mc.cell_width = 5
        self.assertEqual('Janu…', mc.pre_render())

        # Пререндер пустой ячейки
        mc = MonthCell(date_=date(2020, 1, 1))
        mc.cell_width = 0
        self.assertEqual('', mc.pre_render())

        # Пререндер ячейки с отрицательной длиной
        mc = MonthCell(date_=date(2020, 1, 1))
        mc.cell_width = -100
        self.assertEqual('', mc.pre_render())

