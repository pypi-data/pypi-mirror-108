import tkinter
from datetime import date, timedelta
from typing import Optional

from svgwrite import Drawing
from svgwrite.path import Path

from linum.svg_renderer.base.style import Style


class GridView:

    def __init__(self, layers_count: int,
                 start: date, length: int,
                 width: Optional[float] = None, style: Optional[Style] = None):
        self.layers_count = layers_count

        self.start = start
        self.length = length

        self.width = width or tkinter.Tk().winfo_screenwidth()
        self.style = style or Style()

    @property
    def cell_width(self):
        return self.width / self.length

    def render(self, drawing: Drawing, x: float, y: float):
        # Getting grid style
        style = self.style.get_sub_style("grid").get("style", "{}")

        # Getting header sizes
        header_style = self.style.get_sub_style("header")
        months_height = header_style.get_sub_style("months").get("height", 100)
        days_height = header_style.get_sub_style("days").get("height", 100)
        weekdays_height = header_style.get_sub_style("weekdays").get("height", 100)

        # Getting layers sizes
        tasks_style = self.style.get_sub_style("layers").get_sub_style("tasks")
        tasks_height = tasks_style.get("height", 100)
        tasks_indent = tasks_style.get("indent", 0)
        layers_height = tasks_indent + self.layers_count * (tasks_height + tasks_indent)

        # Left border
        height = months_height + days_height + weekdays_height + layers_height
        left_border = Path(["M", x, y, "L", x, y + height],
                           class_=" ".join(["grid", "left", "vertical", "border"]),
                           style=style)
        drawing.add(left_border)

        # Vertical Inner borders
        for offset in range(1, self.length):
            d = self.start + timedelta(offset)

            y_ = y + months_height
            height = days_height + weekdays_height + layers_height
            if d.day == 1:
                y_ -= months_height
                height += months_height

            x_ = x + self.cell_width * offset

            border = Path(["M", x_, y_, "L", x_, y_ + height],
                          class_=" ".join(["grid", "inner", "vertical", "border"]),
                          style=style)
            drawing.add(border)

        # Right border
        x_ = x + self.length * self.cell_width
        height = months_height + days_height + weekdays_height + layers_height
        right_border = Path(["M", x_, y, "L", x_, y + height],
                            class_=" ".join(["grid", "right", "vertical", "border"]),
                            style=style)
        drawing.add(right_border)

        # Top borders
        top_border = Path(["M", x, y, "L", x + self.width, y],
                          class_=" ".join(["grid", "top", "horizontal", "border"]),
                          style=style)
        drawing.add(top_border)

        # Border between months and days
        y_ = y + months_height
        border = Path(["M", x, y_, "L", x + self.width, y_],
                      class_=" ".join(["grid", "inner", "horizontal", "month", "days", "border"]),
                      style=style)
        drawing.add(border)

        # Border under header
        y_ = y + months_height + days_height + weekdays_height
        header_border = Path(["M", x, y_, "L", x + self.width, y_],
                             class_=" ".join(["grid", "inner", "horizontal", "header", "border"]),
                             style=style)
        drawing.add(header_border)

        # Bottom border
        y_ = y + months_height + days_height + weekdays_height + layers_height
        bottom_border = Path(["M", x, y_, "L", x + self.width, y_],
                             class_=" ".join(["grid", "bottom", "horizontal", "border"]),
                             style=style)
        drawing.add(bottom_border)
