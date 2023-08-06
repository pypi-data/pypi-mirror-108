from datetime import date, timedelta
from typing import List, Any

from .border import Border
from .date_cell import DateCell
from .row import Row


class DateRow(Row):

    def __init__(self, start_date: date, length: int):
        """
        Строка работающая с датами.

        :param start_date:
        :param length:
        """
        self.start_date = start_date
        self.length = length

        self.cell_width = 4

        self.month_inner_borders = False
        self.month_inner_border_char = Border(t=True, b=True)

        super().__init__()

    def __repr__(self):
        return "<DateRow: with {} cells>".format(len(self.cells))

    @property
    def date_cell_class(self):
        return DateCell

    @property
    def cells(self) -> List[DateCell]:
        """
        Возвращает список с ячейками-датами.

        :return: List[DayCell]
        """
        if self.length <= 0:
            return []

        # Формируем ячейки
        dates = [self.start_date + timedelta(i) for i in range(self.length)]
        cells = [self.date_cell_class(self.cell_width, d) for d in dates]

        # Устанавливаем границы между месяцами
        if not self.inner_borders and self.month_inner_borders:
            cells = self.set_month_borders(cells, self.month_inner_border_char)

        return cells

    @cells.setter
    def cells(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_:
        """
        pass

    @staticmethod
    def set_month_borders(cells: List[DateCell], border=Border(t=True, b=True)) -> List[DateCell]:
        """
        Устанавливает границы между месяцами.

        :param cells: ячейки для установки границ
        :param border: граница, которую необходимо установить
        :return: List[DateCell]
        """
        for i in range(1, len(cells)):
            if cells[i].date.day == 1:
                cells[i].left_border = True
                cells[i].left_border_char += border

                cells[i - 1].right_border = True
                cells[i - 1].right_border_char += border

        return cells
