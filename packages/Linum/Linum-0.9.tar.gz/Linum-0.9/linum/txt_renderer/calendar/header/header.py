from datetime import date

from linum.txt_renderer.base.border import Border
from .day.days_row import DaysRow
from .month.months_row import MonthsRow
from .weekday.weekdays_row import WeekdaysRow


class Header:

    def __init__(self, start_date: date = date.today(), length: int = 0):
        """
        Заголовок с датами.

        :param start_date: начальная дата отображения
        :param length: количество дней для отображения
        """
        self.start_date = start_date
        self.length = length

        self.cell_width = 4

        self.left_border = False
        self.right_border = False
        self.month_inner_borders = False
        self.inner_borders = False

        self.month_inner_border_char = Border(t=True, b=True)
        self.left_border_char = Border(t=True, b=True)
        self.right_border_char = Border(t=True, b=True)
        self.inner_border_char = Border(t=True, b=True)

    def render_months(self) -> str:
        return self._render_segment(MonthsRow)

    def render_days(self) -> str:
        return self._render_segment(DaysRow)

    def render_weekdays(self) -> str:
        return self._render_segment(WeekdaysRow)

    def render(self) -> str:
        """
        Рендер заголовка с датами.
        Возвращает строковое представление этого заголовка.

        :return:
        """
        s = '\n'.join([self.render_months(), self.render_days(), self.render_weekdays()])
        return s

    def _render_segment(self, segment_type) -> str:
        segment = segment_type(self.start_date, self.length)
        segment.cell_width = self.cell_width

        # Устанавливаем левую границу
        segment.left_border = self.left_border
        segment.left_border_char = self.left_border_char

        # Устанавливаем правую границу
        segment.right_border = self.right_border
        segment.right_border_char = self.right_border_char

        # Устанавливаем границы между ячейками
        segment.inner_borders = self.inner_borders
        segment.inner_border_char = self.inner_border_char

        # Устанавливаем границы между месяцами
        segment.month_inner_borders = self.month_inner_borders
        segment.month_inner_border_char = self.month_inner_border_char

        return segment.render()
