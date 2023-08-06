from datetime import date
from typing import Any, Optional

from linum.txt_renderer.base.date_cell import DateCell


class DayCell(DateCell):

    def __init__(self, cell_width: int = 0, date_: Optional[date] = None):
        """
        Ячейка с порядковым номером дня в месяце.

        :param cell_width: ширина ячейки в символах;
        :param date_: дата, которую необходимо отобразить.
        """
        super().__init__(cell_width, date_)

    def __repr__(self):
        return "<Day: {}>".format(self.content)

    @property
    def content(self):
        """
        Возвращает день месяца ячейки.

        :return: date
        """
        if isinstance(self.date, date):
            return str(self.date.day)
        return ''

    @content.setter
    def content(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_: Any
        """
        pass
