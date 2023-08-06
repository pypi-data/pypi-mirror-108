from datetime import date
from typing import Any, Optional

from .cell import Cell


class DateCell(Cell):

    def __init__(self, cell_width: int = 0, date_: Optional[date] = None):
        """
        Ячейка с датой.

        :param cell_width: ширина ячейки в символах;
        :param date_: дата ячейки.
        """
        self.date = date_
        super().__init__(cell_width)

    def __repr__(self):
        return "<DateCell: {}>".format(self.content)

    @property
    def content(self):
        """
        Возвращает день месяца ячейки.

        :return: date
        """
        if isinstance(self.date, date):
            return str(self.date)
        return ''

    @content.setter
    def content(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_: Any
        """
        pass
