from datetime import date
from typing import Optional, Any, List

from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.cell import Cell
from linum.excel_renderer.base.style import Style


class DateCell(Cell):

    def __init__(self, date_: date = date.today(),
                 style: Optional[Style] = None):
        """
        Cell with date as content.

        :param date_: date content
        :param style: xlsxwriter and other params to apply
        """
        super().__init__(style=style)
        self.date = date_

    @property
    def num_format(self) -> str:
        """
        Numeric format for date. Need to be overridden.

        :return: str
        """
        return ''

    @property
    def content(self) -> date:
        return self.date

    @content.setter
    def content(self, value: Any):
        pass

    @staticmethod
    def get_render_method(worksheet: Worksheet):
        return worksheet.write_datetime

    def pre_render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook) -> Format:
        self.style.update({'num_format': self.num_format})
        return super().pre_render(row, column, worksheet, workbook)
