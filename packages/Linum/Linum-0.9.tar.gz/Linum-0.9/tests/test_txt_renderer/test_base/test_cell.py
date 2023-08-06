from unittest import TestCase

from linum.txt_renderer.base.cell import Cell
from linum.txt_renderer.enums import Align


class TestCell(TestCase):

    def setUp(self) -> None:
        self.cell = Cell(4)

    def test_render(self):
        # Рендер пустой ячейки
        self.assertEqual('    ', self.cell.render())

        # Ячейка нулевой длины
        self.cell.cell_width = 0
        self.assertEqual('', self.cell.render())

        # Ячейка отрицательной длины
        self.cell.cell_width = -1
        self.assertEqual('', self.cell.render())

        # Рендер заполненой ячейки
        self.cell.cell_width = 4
        self.cell.content = '1234'
        self.assertEqual('1234', self.cell.render())

        # Рэндер ячейки с содержимым, превышающим размеры ячейки
        self.cell.content = '12345'
        self.assertEqual('123…', self.cell.render())

        # Центрирование
        self.cell.content = 'C'
        self.cell.align = Align.CENTER
        self.assertEqual(' C  ', self.cell.render())

        # Центрирование вправо
        self.cell.content = 'R'
        self.cell.align = Align.RIGHT
        self.assertEqual('   R', self.cell.render())

        # Центрирование влево
        self.cell.content = 'L'
        self.cell.align = Align.LEFT
        self.assertEqual('L   ', self.cell.render())

        # Левая граница
        self.cell.left_border = True
        self.assertEqual('│L   ', self.cell.render())

        # Правая граница
        self.cell.left_border = False
        self.cell.right_border = True
        self.assertEqual('L   │', self.cell.render())

        # Обе границы
        self.cell.left_border = True
        self.assertEqual('│L   │', self.cell.render())


