from datetime import date

from linum.txt_renderer.base.date_row import DateRow
from .weekday_cell import WeekdayCell


class WeekdaysRow(DateRow):

    def __init__(self, start_date: date = date.today(), length: int = 0):
        """
        Строка с днями недели.

        :param start_date: начальная дата для отображения в качестве дня недели
        :param length: количество отображаемых дней
        """
        super().__init__(start_date=start_date, length=length)

    def __repr__(self):
        return "<WeekdaysRow: '{}'>".format(self.start_date.strftime('%B'))

    @property
    def date_cell_class(self):
        return WeekdayCell
