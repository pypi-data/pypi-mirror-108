from datetime import date
from typing import Optional, List

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.style import Style


class DayCell(DateCell):

    def __init__(self, date_: date = date.today(), style: Optional[Style] = None):
        """
        Cell with day of date.

        :param date_: date content
        :param style: xlsxwriter and other params to apply
        """
        super().__init__(date_, style)

    @property
    def num_format(self) -> str:
        return 'd'
