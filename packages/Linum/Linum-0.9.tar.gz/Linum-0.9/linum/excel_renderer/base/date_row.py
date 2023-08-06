from datetime import date, timedelta
from typing import List, Optional, Any, Type

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.row import Row
from linum.excel_renderer.base.style import Style
from linum.helper import is_day_off


class DateRow(Row):

    def __init__(self, date_: date, length: int,
                 days_off: Optional[List[date]] = None, workdays: Optional[List[date]] = None,
                 workday_style: Optional[Style] = None, day_off_style: Optional[Style] = None):
        """
        Row with dates content.

        :param date_: start date
        :param length: length of period
        :param days_off: list of days-off
        :param workdays: list of workdays
        :param workday_style: style to apply for workdays
        :param day_off_style: style to apply for days-off
        """
        self.day_off_style = day_off_style or Style()
        self.workday_style = workday_style or Style()

        self.date = date_
        self.length = length

        self.workdays = workdays or []
        self.days_off = days_off or []

    @property
    def cells(self) -> List[DateCell]:
        cells = [self._date_cell_class(self.date + timedelta(i)) for i in range(self.length)]
        for cell in cells:
            if is_day_off(cell.date, self.days_off, self.workdays):
                cell.style = self.day_off_style
            else:
                cell.style = self.workday_style
        return cells

    @cells.setter
    def cells(self, any_: Any):
        pass

    @property
    def _date_cell_class(self) -> Type[DateCell]:
        return DateCell
