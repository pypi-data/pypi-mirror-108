from typing import Optional

from xlsxwriter import Workbook
from xlsxwriter.format import Format
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.style import Style


class Cell:

    def __init__(self, content: str = '', style: Optional[Style] = None):
        """
        Excel base cell.

        :param content: cell string content
        :param style: dict of xlsxwriter and other params to apply
        """
        self.content = content
        self.style = style or Style()

    @staticmethod
    def get_render_method(worksheet: Worksheet):
        """
        Returns xlsxwriter method to write data.

        :param worksheet: xlsxwriter worksheet
        """
        return worksheet.write

    def pre_render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook) -> Format:
        """
        Sets cell size and prepares style settings.

        """
        # Setting cell height
        cell_height_px = self.style.get("cell_height_px", None)
        if isinstance(cell_height_px, int):
            cell_height_px = max(0, cell_height_px)
            worksheet.set_row_pixels(row, cell_height_px)

        # Setting cell width
        cell_width_px = self.style.get('cell_width_px', None)
        if isinstance(cell_width_px, int):
            cell_width_px = max(0, cell_width_px)
            worksheet.set_column_pixels(column, column, cell_width_px)

        # Getting format
        format_ = self.style.get_xlsxwriter_format(workbook)

        return format_

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook):
        """
        Renders cell in specified place.

        :param row: zero-based row index
        :param column: zero-based column index
        :param worksheet: xlsxwriter worksheet
        :param workbook: xlsxwriter workbook
        """
        # Pre rendering
        format_ = self.pre_render(row, column, worksheet, workbook)

        # Rendering
        render_method = self.get_render_method(worksheet)
        render_method(row, column, self.content, format_)
