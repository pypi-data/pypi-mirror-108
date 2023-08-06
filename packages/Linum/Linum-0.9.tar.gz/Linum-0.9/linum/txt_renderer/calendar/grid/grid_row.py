from datetime import date
from typing import Any, List

from linum.txt_renderer.base.border import Border
from linum.txt_renderer.base.date_cell import DateCell
from linum.txt_renderer.base.date_row import DateRow
from .grid_cell import GridCell


class GridRow(DateRow):

    def __init__(self, start_date: date = date.today(), length: int = 0, top_outline: bool = True):
        """
        Строка сетки.

        :param start_date: начальная дата
        :param length: продолжительность
        """
        super().__init__(start_date, length)
        self.top_outline = top_outline
        self.inner_border_char = Border(t=top_outline, b=not top_outline)
        self.month_inner_border_char = Border(t=top_outline, b=not top_outline)
        self.left_border_char = Border(r=True, b=top_outline, t=not top_outline)
        self.right_border_char = Border(l=True, b=top_outline, t=not top_outline)

    @property
    def cells(self) -> List[DateCell]:
        cells = super().cells
        if not cells:
            return []
        if self.inner_borders:
            for i in range(1, len(cells)):
                cells[i].left_border = True
                cells[i - 1].right_border = True
        return cells

    @cells.setter
    def cells(self, any_: Any):
        """
        Заглушка. Не вносит никаких изменений.
        Необходима для корректного вызова конструктора родительского класса.

        :param any_:
        """
        pass

    @property
    def date_cell_class(self):
        return GridCell
