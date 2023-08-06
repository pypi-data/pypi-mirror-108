from typing import List, Optional

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.cell import Cell


class Row:

    def __init__(self, cells: Optional[List[Cell]] = None):
        """
        Base excel row.

        :param cells: sequence of cells
        """
        self.cells = cells or []

    def pre_render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook) -> List[Cell]:
        """
        Pre render row. May be overriding to control cells style.

        :param row: zero-based row index
        :param column: zero-based column index
        :param worksheet: xlsxwriter worksheet
        :param workbook: xlsxwriter workbook
        """
        return self.cells

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook):
        """
        Renders row.

        :param row: zero-based row index
        :param column: zero-based column index
        :param worksheet: xlsxwriter worksheet
        :param workbook: xlsxwriter workbook
        """
        cells = self.pre_render(row, column, worksheet, workbook)
        for i, cell in enumerate(cells):
            cell.render(row, column + i, worksheet, workbook)
