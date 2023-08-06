from typing import Any

from linum.txt_renderer.enums import Align
from linum.helper import supp_content, trim_content
from .border import Border


class Cell:

    def __init__(self, cell_width: int = 0, content: Any = ''):
        """
        Ячейка.

        :param cell_width: ширина ячейки в символах;
        :param content: текстовое содержимое.
        """
        self.cell_width = cell_width
        self.content = content

        self.left_border = False
        self.right_border = False

        self.left_border_char = Border(t=True, b=True)
        self.right_border_char = Border(t=True, b=True)

        self.fill_char = Border()

        self.align: Align = Align.CENTER

    def __repr__(self):
        return "<Cell: '{}' with width {}>".format(self.content, self.cell_width)

    def __len__(self):
        return len(self.render())

    def __bool__(self):
        if self.cell_width <= 0:
            return False
        return True

    def __eq__(self, other):
        if not isinstance(other, Cell):
            return False
        for k, v in self.__dict__.items():
            if getattr(other, k) != v:
                return False
        return True

    def draw_over(self, content: str) -> None:
        """
        Устанавливает содержимое ячейки поверх предыдущего значения.

        :param content: новое содержимое;
        """
        chars = list(self.content)
        self.content = ''.join([content] + chars[len(content):])

    def pre_render(self) -> str:
        """
        Предварительный рендер содержимого ячейки.
        Возвращает строковое представление содержимого без границ.

        :return: str
        """
        content = str(self.content)
        content = supp_content(content, self.cell_width, self.align, str(self.fill_char))
        content = trim_content(content, self.cell_width)
        return content

    def render(self) -> str:
        """
        Возвращает ASCII представление ячейки.

        :return: str
        """
        s = self.pre_render()

        # Рисуем границы ячейки.
        if self.left_border:
            s = str(self.left_border_char) + s
        if self.right_border:
            s += str(self.right_border_char)
        return s
