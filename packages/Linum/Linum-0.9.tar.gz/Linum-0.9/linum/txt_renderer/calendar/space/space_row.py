from datetime import date

from linum.txt_renderer.base.date_row import DateRow
from .space_cell import SpaceCell


class SpaceRow(DateRow):

    def __init__(self, start_date: date, length: int):
        """
        Пробельная строка. Отделяет кусочки задач на слое.

        :param start_date:
        :param length:
        """
        super().__init__(start_date, length)

    @property
    def date_cell_class(self):
        return SpaceCell
