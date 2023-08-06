from typing import Type

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.date_row import DateRow
from .day_cell import DayCell


class DaysRow(DateRow):

    @property
    def _date_cell_class(self) -> Type[DateCell]:
        return DayCell
