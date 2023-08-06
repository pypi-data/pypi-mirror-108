from datetime import date
from typing import Type, Optional, List

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.date_row import DateRow
from linum.excel_renderer.base.style import Style
from linum.helper import split_by_months
from .month_cell import MonthCell
from ...space.space_row import SpaceRow


class MonthsRow(DateRow):

    def __init__(self, date_: date, length: int, style: Optional[Style] = None):
        """
        Row with months cells.

        :param date_:
        :param length:
        :param style:
        """
        super().__init__(date_, length, [], [], style, None)

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook):
        months = split_by_months(self.date, self.length)
        offset = 0
        for d, length in months:
            # Rendering background
            bg_row = SpaceRow(d, length, workday_style=self.workday_style, day_off_style=self.workday_style)
            bg_row.render(row, column + offset, worksheet, workbook)

            worksheet.merge_range(row, column + offset, row, column + offset + length - 1, '')
            cell = MonthCell(d, self.workday_style)
            cell.render(row, column + offset, worksheet, workbook)
            offset += length

    @property
    def _date_cell_class(self) -> Type[DateCell]:
        return MonthCell
