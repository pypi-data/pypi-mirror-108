from datetime import date
from typing import Optional, List

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.style import Style
from linum.excel_renderer.calendar.header.day.days_row import DaysRow
from linum.excel_renderer.calendar.header.month.months_row import MonthsRow
from linum.excel_renderer.calendar.header.weekday.weekdays_row import WeekdaysRow


class Header:

    def __init__(self, start_date: date, length: int,
                 days_off: Optional[List[date]] = None, workdays: Optional[List[date]] = None,
                 header_style: Optional[Style] = None, days_off_header_style: Optional[Style] = None):
        """
        Header with dates.

        :param start_date: date from which the rendering will start
        :param length: days count
        :param days_off: list of days-off dates
        :param workdays: list of workdays dates
        :param header_style: header style for workdays
        :param days_off_header_style: header style for days-off
        """
        self.start_date = start_date
        self.length = length

        self.days_off = days_off
        self.workdays = workdays

        self.header_style = header_style
        self.days_off_header_style = days_off_header_style

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook):
        # Preparing months row
        months_style = self.header_style.get_sub_style("months")
        mr = MonthsRow(self.start_date, self.length, months_style)

        # Preparing days row
        days_style = self.header_style.get_sub_style("days")
        days_off_days_style = self.days_off_header_style.get_sub_style("days")
        days_off_days_style.parents.insert(0, days_style)
        dr = DaysRow(self.start_date, self.length, self.days_off, self.workdays,
                     days_style, days_off_days_style)

        # Preparing weekdays row
        weekdays_style = self.header_style.get_sub_style("weekdays")
        days_off_weekdays_style = self.days_off_header_style.get_sub_style("weekdays")
        days_off_weekdays_style.parents.insert(0, weekdays_style)
        wr = WeekdaysRow(self.start_date, self.length, self.days_off, self.workdays,
                         weekdays_style, days_off_weekdays_style)

        # Rendering
        mr.render(row, column, worksheet, workbook)
        dr.render(row + 1, column, worksheet, workbook)
        wr.render(row + 2, column, worksheet, workbook)
