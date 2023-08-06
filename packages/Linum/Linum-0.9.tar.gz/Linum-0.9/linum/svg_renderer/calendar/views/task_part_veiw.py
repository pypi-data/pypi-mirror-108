from typing import Optional, Any

from svgwrite import Drawing

from linum.color import Color
from linum.svg_renderer.base.cell import Cell
from linum.svg_renderer.base.style import Style
from linum.task_part import TaskPart


class TaskPartView(Cell):

    def __init__(self, task_part: TaskPart, cell_width: float, style: Optional[Style] = None):
        self.task_part = task_part
        self.cell_width = cell_width
        super().__init__("", 0, style, [task_part.task.name])

    @classmethod
    def get_class(cls) -> str:
        return "task"

    @property
    def content(self) -> str:
        return self.task_part.task.name

    @content.setter
    def content(self, any_: Any):
        pass

    @property
    def width(self) -> float:
        return self.task_part.length * self.cell_width

    @width.setter
    def width(self, any_: Any):
        pass

    @property
    def height(self) -> int:
        return self.style.get("height", 100)

    def render(self, drawing: Drawing, x: float, y: float):
        # Background color
        color = self.task_part.task.color
        bg = self.style.setdefault("background", Style("background"))
        bg.update({"color": color})

        # Text color
        if self.style.get("auto-font-color", False):
            font_color = Color(color).get_contrast_font_color()
            text_style = self.style.setdefault("text", Style("text"))
            text_style.update({"style": "fill: {}".format(str(font_color))})
        super().render(drawing, x, y)
