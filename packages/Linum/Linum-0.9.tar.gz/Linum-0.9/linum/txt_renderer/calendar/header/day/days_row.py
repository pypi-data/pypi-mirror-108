from datetime import date

from linum.txt_renderer.base.date_row import DateRow
from .day_cell import DayCell


class DaysRow(DateRow):

    def __init__(self, start_date: date, length: int):
        """
        Строка с числами месяца.

        :param start_date: начальная дата строки
        :param length: продолжительность строки в днях
        """
        super().__init__(start_date, length)

    def __repr__(self):
        return "<DaysRow: '{}'>".format(self.start_date.strftime('%B'))

    @property
    def date_cell_class(self):
        return DayCell
