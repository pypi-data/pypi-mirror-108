import tkinter
from datetime import date
from typing import Optional

from svgwrite import Drawing

from linum.svg_renderer.base.style import Style
from linum.svg_renderer.calendar.header.day.days_row import DaysRow
from linum.svg_renderer.calendar.header.month.months_row import MonthsRow
from linum.svg_renderer.calendar.header.weekday.weekdays_row import WeekdaysRow


class Header:

    def __init__(self, start: date, length: int, width: Optional[float] = None,
                 header_style: Optional[Style] = None):
        self.width = width or tkinter.Tk().winfo_screenwidth()

        self.start = start
        self.length = length

        self.header_style = header_style or Style('default header')

    @property
    def height(self) -> int:
        height = self.header_style.get_sub_style("days").get("height", 100) \
                 + self.header_style.get_sub_style("weekdays").get("height", 100) \
                 + self.header_style.get_sub_style("months").get("height", 100)

        return height

    def render(self, drawing: Drawing, x: int, y: int):
        months_style = self.header_style.get_sub_style("months")
        mr = MonthsRow(self.start, self.length, self.width, months_style)

        days_style = self.header_style.get_sub_style("days")
        dr = DaysRow(self.start, self.length, self.width,
                     days_style)

        weekdays_style = self.header_style.get_sub_style("weekdays")
        wr = WeekdaysRow(self.start, self.length, self.width,
                         weekdays_style)

        mr.render(drawing, x, y)
        dr.render(drawing, x, y + mr.height)
        wr.render(drawing, x, y + mr.height + dr.height)
