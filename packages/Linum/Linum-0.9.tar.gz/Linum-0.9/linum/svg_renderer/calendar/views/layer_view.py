import tkinter
from datetime import date, timedelta
from typing import Optional, List

from svgwrite import Drawing
from svgwrite.shapes import Rect

from linum.layer import Layer
from linum.svg_renderer.base.style import Style
from linum.svg_renderer.calendar.views.task_part_veiw import TaskPartView


class LayerView:

    def __init__(self, layer: Layer, start: date, length: int,
                 width: Optional[int] = None, style: Optional[Style] = None):
        self.length = length
        self.start = start
        self.layer = self._trim_layer(layer)

        self.width = width or tkinter.Tk().winfo_screenwidth()
        self.style = style or Style()

    @property
    def height(self):
        return self.style.get("height", 100)

    def render(self, drawing: Drawing, x: float, y: float):
        # Rendering background
        background = Rect(insert=(x, y),
                          size=(self.width, self.height),
                          class_=" ".join(["layer", "background"]),
                          debug=False)
        drawing.add(background)

        # Rendering task parts
        cell_width = self.width / self.length
        for part in self.layer.parts:
            x_ = cell_width * (part.start - self.start).days
            tpv = TaskPartView(part, cell_width, self.style)
            tpv.render(drawing, x_ + x, y)

    def _trim_layer(self, layer: Layer) -> Layer:
        _, layer = layer.split(self.start)
        layer, _ = layer.split(self.start + timedelta(self.length))
        return layer
