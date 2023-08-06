from datetime import date
from typing import Any

from linum.txt_renderer.base.border import Border
from linum.txt_renderer.base.date_cell import DateCell


class GridCell(DateCell):

    def __init__(self, cell_width: int = 0, date_: date = date.today):
        """
        Сеточная ячейка. Нужна для рисования сеток.

        :param cell_width: ширина ячейки в символах
        :param date_: дата ячейки
        """
        super().__init__(cell_width, date_)
        self.left_border_char = Border(r=True)
        self.right_border_char = Border(l=True)
        self.fill_char = Border(l=True, r=True)

    @property
    def content(self) -> str:
        """
        Возвращает символьное представление ячейки.

        :return: str
        """
        return self.cell_width * str(self.fill_char)

    @content.setter
    def content(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_:
        """
        pass
