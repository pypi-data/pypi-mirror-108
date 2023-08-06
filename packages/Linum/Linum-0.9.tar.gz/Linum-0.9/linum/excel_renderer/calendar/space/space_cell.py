from datetime import date
from typing import Optional

from linum.excel_renderer.base.cell import Cell
from linum.excel_renderer.base.style import Style


class SpaceCell(Cell):

    def __init__(self, date_: date, content: str = '', style: Optional[Style] = None):
        self.date = date_
        super().__init__(content, style)
