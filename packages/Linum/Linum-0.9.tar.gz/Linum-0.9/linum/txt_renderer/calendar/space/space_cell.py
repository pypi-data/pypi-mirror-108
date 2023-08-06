from datetime import date
from typing import Optional, Any

from linum.txt_renderer.base.date_cell import DateCell


class SpaceCell(DateCell):

    def __init__(self, cell_width: int = 0, date_: Optional[date] = None):
        """
        Пробельная ячейка. Разделяет кусочки задач на слое.

        :param cell_width: ширина ячейки в символах
        :param date_: дата ячейки
        """
        super().__init__(cell_width, date_)

    @property
    def content(self):
        return ''

    @content.setter
    def content(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_: Any
        """
        pass
