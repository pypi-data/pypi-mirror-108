from unittest import TestCase

from linum.txt_renderer.calendar.grid.grid_cell import GridCell


class TestGridCell(TestCase):

    def test_prerender(self):
        # Пререндер пустой ячейки
        gc = GridCell()
        self.assertEqual('', gc.pre_render())

        # Пререндер обычной ячейки
        gc = GridCell(cell_width=1)
        self.assertEqual('─', gc.pre_render())

        # Преендер обычной ячейки двойной ширины
        gc = GridCell(cell_width=2)
        self.assertEqual('──', gc.pre_render())

        # Пререндер ячейки с границами
        gc.left_border = True
        gc.right_border = True
        self.assertEqual('──', gc.pre_render())

    def test_render(self):
        # Рендер пустой ячейки
        gc = GridCell()
        self.assertEqual('', gc.render())

        # Рендер пустой ячейки
        gc = GridCell(cell_width=1)
        self.assertEqual('─', gc.render())

        # Рендер пустой ячейки двойной ширины
        gc = GridCell(cell_width=2)
        self.assertEqual('──', gc.render())

        # Рендер ячейки с границами
        gc.left_border = True
        gc.right_border = True
        self.assertEqual('╶──╴', gc.render())
