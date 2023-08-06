from datetime import date, timedelta
from typing import List, Optional

from linum.svg_renderer.base.row import Row
from linum.svg_renderer.base.style import Style
from linum.svg_renderer.calendar.header.weekday.weekday_cell import WeekdayCell


class WeekdaysRow(Row):

    def __init__(self, start: date, length: int, width: float,
                 style: Optional[Style] = None):
        self.start = start
        self.length = length
        self.width = width

        self.style = style or Style("default workday")

    @property
    def height(self) -> int:
        height = self.style.get("height", 100)
        return height

    @property
    def cells(self) -> List[WeekdayCell]:
        cells = []
        cell_width = self.width / self.length
        for offset in range(self.length):
            d = self.start + timedelta(offset)
            cell = WeekdayCell(d, cell_width, self.style)
            cells.append(cell)
        return cells
