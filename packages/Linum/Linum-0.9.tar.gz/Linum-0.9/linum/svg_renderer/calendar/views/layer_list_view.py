import tkinter
from datetime import date, timedelta
from typing import Optional

from svgwrite import Drawing
from svgwrite.shapes import Rect

from linum.layer_list import LayerList
from linum.svg_renderer.base.style import Style
from linum.svg_renderer.calendar.views.layer_view import LayerView


class LayerListView:

    def __init__(self, layer_list: LayerList, start: date, length: int,
                 width: Optional[float] = None,
                 tasks_style: Optional[Style] = None):
        self.start = start
        self.length = length

        self.layer_list = self._trim_and_clean(layer_list)

        self.width = width or tkinter.Tk().winfo_screenwidth()
        self.tasks_style = tasks_style or Style("default layers")

    @property
    def height(self):
        layer_height = self.tasks_style.get("height", 100)
        indent = self.tasks_style.get("indent", 0)
        return len(self.layer_list.layers) * (layer_height + indent) + indent

    def render(self, drawing: Drawing, x: float, y: float):
        # Rendering first indent
        indent = self.tasks_style.get("indent", 0)
        indent_background = Rect(insert=(x, y),
                                 size=(self.width, indent),
                                 class_=" ".join(["layer", "indent", "background"]),
                                 debug=False)
        drawing.add(indent_background)

        y_ = y + indent
        for layer in self.layer_list.layers:
            # Rendering layer
            lv = LayerView(layer, self.start, self.length, self.width, self.tasks_style)
            lv.render(drawing, x, y_)

            # Rendering indent
            indent_background = Rect(insert=(x, y_ + lv.height),
                                     size=(self.width, indent),
                                     class_=" ".join(["layer", "indent", "background"]),
                                     debug=False)
            drawing.add(indent_background)

            y_ += lv.height + indent

    def _trim_and_clean(self, layer_list: LayerList) -> LayerList:
        _, ll = layer_list.split(self.start)
        ll, _ = ll.split(self.start + timedelta(self.length))
        ll.cleanup()
        return ll
