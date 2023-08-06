from datetime import date
from typing import Any, Optional

from linum.svg_renderer.base.cell import Cell
from linum.svg_renderer.base.style import Style


class MonthCell(Cell):

    def __init__(self, date_: date, width: float,
                 style: Optional[Style] = None):
        self.date_ = date_
        super().__init__("", width, style)

    @property
    def content(self):
        return self.date_.strftime("%B `%y")

    @content.setter
    def content(self, any_: Any):
        pass

    @classmethod
    def get_class(cls):
        return "header month"
