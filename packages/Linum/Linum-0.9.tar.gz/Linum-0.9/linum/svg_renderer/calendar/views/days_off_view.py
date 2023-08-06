import tkinter
from datetime import date, timedelta
from typing import Optional, List

from svgwrite.shapes import Rect

from linum import helper
from svgwrite import Drawing

from linum.excel_renderer.base.style import Style


class DaysOffView:

    def __init__(self, layers_count: int,
                 start: date, length: int,
                 width: Optional[float] = None, style: Optional[Style] = None,
                 workdays: Optional[List[date]] = None, days_off: Optional[List[date]] = None):
        self.layers_count = layers_count

        self.start = start
        self.length = length

        self.width = width or tkinter.Tk().winfo_screenwidth()
        self.style = style or Style()

        self.workdays = workdays or []
        self.days_off = days_off or []

    @property
    def cell_width(self):
        return self.width / self.length

    def render(self, drawing: Drawing, x: float, y: float):
        # Getting header sizes
        header_style = self.style.get_sub_style("header")
        months_height = header_style.get_sub_style("months").get("height", 100)
        days_height = header_style.get_sub_style("days").get("height", 100)
        weekdays_height = header_style.get_sub_style("weekdays").get("height", 100)

        # Getting layers sizes
        tasks_style = self.style.get_sub_style("layers").get_sub_style("tasks")
        tasks_height = tasks_style.get("height", 100)
        tasks_indent = tasks_style.get("indent", 0)
        layers_height = tasks_indent + self.layers_count * (tasks_height + tasks_indent)

        y_ = y + months_height
        days_off_height = days_height + weekdays_height + layers_height
        for offset in range(self.length):
            d = self.start + timedelta(offset)
            if helper.is_day_off(d, self.days_off, self.workdays):
                x_ = x + offset * self.cell_width
                rect = Rect(insert=(x_, y_),
                            size=(self.cell_width, days_off_height),
                            class_=" ".join(["day-off"]),
                            debug=False)
                drawing.add(rect)

        # drawing.save(pretty=True)  # too slow to be here
