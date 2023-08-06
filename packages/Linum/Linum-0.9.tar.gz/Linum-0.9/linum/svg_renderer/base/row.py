from typing import List, Optional

from svgwrite import Drawing

from linum.svg_renderer.base.cell import Cell


class Row:

    def __init__(self, cells: Optional[List[Cell]]):
        self.cells = cells or []

    def render(self, drawing: Drawing, x: int, y: int):
        max_height = max([cell.height for cell in self.cells])
        for cell in self.cells:
            valign = cell.style.get("valign", "top")
            if valign == "vcenter":
                y_ = y + max_height / 2 - cell.height / 2
            elif valign == "bottom":
                y_ = y + max_height - cell.height
            else:
                y_ = y
            cell.render(drawing, x, y_)
            x += cell.width
