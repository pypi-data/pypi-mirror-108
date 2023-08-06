from datetime import date
from typing import Optional, Any

from linum.txt_renderer.base.date_cell import DateCell


class WeekdayCell(DateCell):

    def __init__(self, cell_width: int = 0, date_: Optional[date] = None):
        """
        Ячейка с названием дня недели.

        :param cell_width: ширина ячейки в символах;
        :param date_: дата, которую необходимо отобразить.
        """
        super().__init__(cell_width, date_)

    def __repr__(self):
        return "<Weekday: {}>".format(self.content)

    @property
    def content(self) -> str:
        """
        Возвращает строку с названием дня недели.

        :return: str
        """
        if isinstance(self.date, date):
            return self.date.strftime("%a")
        return ''

    @content.setter
    def content(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_: Any
        """
        pass
