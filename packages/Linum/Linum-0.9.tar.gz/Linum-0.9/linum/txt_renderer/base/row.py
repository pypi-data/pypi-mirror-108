from typing import List, Union, Optional

from linum.txt_renderer.enums import Align
from .border import Border
from .cell import Cell


class Row:

    def __init__(self, cells: Optional[List[Cell]] = None):
        """
        Строка.

        :param cells: список ячеек для отображения.
        """
        self.cells = cells or []

        self.left_border = False
        self.right_border = False
        self.inner_borders = False

        self.left_border_char = Border(t=True, b=True)
        self.right_border_char = Border(t=True, b=True)
        self.inner_border_char = Border(t=True, b=True)

        self.align: Align = Align.CENTER

    def __repr__(self):
        return "<Row: with {} cells>".format(len(self.cells))

    def __len__(self):
        return len(self.render())

    def __getitem__(self, item):
        return self.cells[item]

    def __add__(self, other):
        if isinstance(other, Row):
            self.cells += other.cells
            return self
        elif isinstance(other, Cell):
            self.cells += [other]
            return self
        raise TypeError("unsupported operand type for +: 'Row' and '{}'".format(type(other)))

    def __bool__(self):
        if not self.cells and not self.left_border and not self.right_border:
            return False
        for cell in self.cells:
            if cell:
                return True
        return False

    def append(self, cells: Union[List[Cell], Cell]):
        """
        Добавляет в конец указанные ячейки.

        :param cells: ячейка или список ячеек для добавления
        """
        if isinstance(cells, list):
            self.cells += cells
        elif isinstance(cells, Cell):
            self.cells.append(cells)

    def pre_render(self) -> Cell:
        """
        Предварительный рендер содержимого строки.
        Возвращает ячейку в которую объединилась строка.

        :return: str
        """
        if len(self.cells) <= 0:
            cell = Cell()
            cell.left_border = self.left_border
            cell.left_border_char = self.left_border_char
            cell.right_border = self.right_border
            cell.right_border_char = self.right_border_char
            return cell

        cells = self.cells
        content = ''
        for i in range(len(cells) - 1):
            content += cells[i].pre_render()

            border = ''
            # Сливаем соседние границы в одну
            if self.inner_borders or cells[i].right_border or cells[i + 1].left_border:
                border = Border()
                if self.inner_borders:
                    border += self.inner_border_char
                if cells[i].right_border:
                    border += cells[i].right_border_char
                if cells[i + 1].left_border:
                    border += cells[i + 1].left_border_char
            content += str(border)
        content += cells[-1].pre_render()

        cell = Cell(len(content), content)

        # Определяем левую границу результирующей ячейки
        cell.left_border = self.left_border or cells[0].left_border
        cell.left_border_char = self.left_border_char
        if cells[0].left_border:
            self.left_border_char += cells[0].left_border_char

        # Определяем правую границу результирующей ячейки
        cell.right_border = self.right_border or cells[-1].right_border
        cell.right_border_char = self.right_border_char
        if cells[-1].right_border:
            self.right_border_char += cells[-1].right_border_char

        return cell

    def render(self) -> str:
        """
        Возвращает символьное представление строки.

        :return: str
        """
        cell = self.pre_render()
        return cell.render()

    def merge(self, content: Optional[str] = None, align: Align = Align.CENTER) -> Cell:
        """
        Объединяет все ячейки строки в одну.
        Если указанно содержимое то оно будет вставлено в результирующую ячейку.
        Если содержимое не указано, то результирующая ячейка будет содержать
        строковое представление строки без внешних границ.

        Значения левой и правой границ наследуются от строки.

        :param content: содержимое для созданной ячейки
        :param align: выравнивание
        :return: Cell
        """
        cell = self.pre_render()

        if content is not None:
            cell.content = content

        cell.align = align

        return cell
