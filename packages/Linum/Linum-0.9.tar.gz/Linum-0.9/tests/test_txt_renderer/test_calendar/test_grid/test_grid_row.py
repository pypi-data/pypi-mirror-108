from unittest import TestCase

from linum.txt_renderer.base.border import Border
from linum.txt_renderer.base.cell import Cell
from linum.txt_renderer.calendar.grid.grid_row import GridRow


class TestGridRow(TestCase):

    def setUp(self) -> None:
        self.cell = Cell()
        self.cell.left_border_char = Border(r=True, b=True)
        self.cell.right_border_char = Border(l=True, b=True)

    def test_prerender(self):
        # Пререндер пустой строки
        gr = GridRow()
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из одной ячейки
        gr = GridRow(length=1)
        gr.cell_width = 3
        self.cell.cell_width = 3
        self.cell.content = '───'
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из двух ячеек
        gr = GridRow(length=2)
        gr.cell_width = 3
        self.cell.cell_width = 6
        self.cell.content = '──────'
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из двух ячеек с внутренней границей
        gr = GridRow(length=2)
        gr.cell_width = 3
        gr.inner_borders = True
        self.cell.cell_width = 7
        self.cell.content = '───┴───'
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из двух ячеек с левой границей без внутренних границ
        gr = GridRow(length=2, top_outline=True)
        gr.cell_width = 3
        gr.left_border = True
        self.cell.cell_width = 6
        self.cell.content = '──────'
        self.cell.left_border = True
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из двух ячеек с левой границей с внутренними границами
        gr = GridRow(length=2, top_outline=True)
        gr.cell_width = 3
        gr.left_border = True
        gr.inner_borders = True
        self.cell.cell_width = 7
        self.cell.content = '───┴───'
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из двух ячеек с правой границой без внутренних границ
        gr = GridRow(length=2, top_outline=True)
        gr.cell_width = 3
        gr.right_border = True
        self.cell.cell_width = 6
        self.cell.content = '──────'
        self.cell.left_border = False
        self.cell.right_border = True
        self.assertEqual(self.cell, gr.pre_render())

        # Пререндер строки из двух ячеек с правой границей с внутренними границами
        gr = GridRow(length=2, top_outline=True)
        gr.cell_width = 3
        gr.right_border = True
        gr.inner_borders = True
        self.cell.cell_width = 7
        self.cell.content = '───┴───'
        self.assertEqual(self.cell, gr.pre_render())

    def test_render(self):
        # Рендер пустой строки
        gr = GridRow()
        self.assertEqual('', gr.render())

        # Рендер строки с одной ячейкой
        gr = GridRow(length=1)
        self.assertEqual('────', gr.render())

        # Рендер строки с одной ячейкой и левой границей
        gr = GridRow(length=1)
        gr.left_border = True
        self.assertEqual('┌────', gr.render())

        # Рендер строки с одной ячейкой и правой границей
        gr = GridRow(length=1)
        gr.right_border = True
        self.assertEqual('────┐', gr.render())

    # def test_merge(self):
    #     self.fail()
