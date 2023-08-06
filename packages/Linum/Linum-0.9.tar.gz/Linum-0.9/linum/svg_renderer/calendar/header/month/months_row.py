from datetime import date
from typing import Optional

from svgwrite import Drawing

from linum.helper import split_by_months
from linum.svg_renderer.base.row import Row
from linum.svg_renderer.base.style import Style
from linum.svg_renderer.calendar.header.month.month_cell import MonthCell


class MonthsRow(Row):

    def __init__(self, start: date, length: int, width: float,
                 style: Optional[Style] = None):
        self.length = length
        self.start = start
        self.width = width

        self.style = style or Style()

    @property
    def height(self) -> int:
        return self.style.get("height", 100)

    def render(self, drawing: Drawing, x: int, y: int):
        months = split_by_months(self.start, self.length)
        cell_width = self.width / self.length
        offset = 0
        for d, length in months:
            mc = MonthCell(d, cell_width * length, self.style)
            mc.render(drawing, x + offset, y)
            offset += cell_width * length
            # drawing.save(pretty=True)  # too slow to be here
