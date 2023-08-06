from datetime import date
from typing import Optional

from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.style import Style


class MonthCell(DateCell):

    def __init__(self, date_: date = date.today(), style: Optional[Style] = None):
        """
        Cell with month name for date.

        :param date_: date to render
        :param style: xlsxwriter and other params to apply
        """
        super().__init__(date_, style)

    @property
    def num_format(self) -> str:
        return 'MMMM `YY'
