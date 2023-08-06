from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.header.month.months_row import MonthsRow


class TestMonthRow(TestCase):

    def test_render(self):
        # Рендер одного месяца
        mr = MonthsRow(date(2020, 1, 31), 1)
        self.assertEqual('Jan…', mr.render())

        # Рендер на границе двух месяцев
        mr = MonthsRow(date(2020, 1, 31), 2)
        self.assertEqual('Jan…Feb…', mr.render())

        # Расширенный рендер на границе месяцев
        mr = MonthsRow(date(2020, 1, 30), 4)
        self.assertEqual('January…Februar…', mr.render())

        # Расширенный рендер на границе месяцев с внутренними границами
        mr = MonthsRow(date(2020, 1, 30), 4)
        mr.inner_borders = True
        self.assertEqual('January …│February…', mr.render())

        # Расширенный рендер на границе месяцев с границами между месяцами
        mr = MonthsRow(date(2020, 1, 30), 4)
        mr.month_inner_borders = True
        self.assertEqual('January…│Februar…', mr.render())

        # Расширенный рендер на границе месяцев с левой границей
        mr = MonthsRow(date(2020, 1, 30), 4)
        mr.left_border = True
        self.assertEqual('│January…Februar…', mr.render())

        # Расширенный рендер на границе месяцев с правой границей
        mr = MonthsRow(date(2020, 1, 30), 4)
        mr.right_border = True
        self.assertEqual('January…Februar…│', mr.render())
