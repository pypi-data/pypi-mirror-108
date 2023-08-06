from datetime import date
from unittest import TestCase

from linum.txt_renderer.calendar.header.weekday.weekdays_row import WeekdaysRow


class TestWeekdaysRow(TestCase):

    def test_render(self):
        # Обычный рендер
        wr = WeekdaysRow(start_date=date(2020, 1, 1), length=7)
        wr.cell_width = 3
        self.assertEqual("WedThuFriSatSunMonTue", wr.render())

        # Рендер строки с пустыми ячейками
        wr = WeekdaysRow(start_date=date(2020, 1, 1), length=7)
        wr.cell_width = 0
        self.assertEqual('', wr.render())

        # Рендер строки на границе месяца без разделительной границы
        wr = WeekdaysRow(start_date=date(2020, 1, 30), length=4)
        wr.cell_width = 3
        self.assertEqual('ThuFriSatSun', wr.render())

        # Рендер строки на границе месяца с разделительной границей
        wr = WeekdaysRow(start_date=date(2020, 1, 30), length=4)
        wr.cell_width = 3
        wr.month_inner_borders = True
        self.assertEqual('ThuFri│SatSun', wr.render())

        # Рендер строки с внутренними границами
        wr = WeekdaysRow(start_date=date(2020, 1, 30), length=4)
        wr.cell_width = 3
        wr.month_inner_borders = False
        wr.inner_borders = True
        self.assertEqual('Thu│Fri│Sat│Sun', wr.render())

