from unittest import TestCase

from linum.txt_renderer.base.cell import Cell
from linum.txt_renderer.base.row import Row


class TestRow(TestCase):

    def setUp(self) -> None:
        self.row = Row()

    def test_render(self):
        # Пустая строка
        self.assertEqual('', self.row.render())

        # строка с одной непустой ячейкой
        cell = Cell(cell_width=4, content='1234')
        self.row.cells.append(cell)
        self.assertEqual('1234', self.row.render())

        # Строка с двумя непустыми ячейками
        cell = Cell(cell_width=4, content='5678')
        self.row.cells.append(cell)
        self.assertEqual('12345678', self.row.render())

        # Левая граница
        self.row.left_border = True
        self.assertEqual('│12345678', self.row.render())

        # Правая граница
        self.row.left_border = False
        self.row.right_border = True
        self.assertEqual('12345678│', self.row.render())

        # Внутренние границы
        self.row.right_border = False
        self.row.inner_borders = True
        self.assertEqual('1234│5678', self.row.render())

        # Все границы
        self.row.left_border = True
        self.row.right_border = True
        self.assertEqual('│1234│5678│', self.row.render())
