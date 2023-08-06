from typing import Optional, List
from uuid import uuid4

from svgwrite import Drawing
from svgwrite.masking import ClipPath
from svgwrite.path import Path
from svgwrite.shapes import Rect
from svgwrite.text import Text

from linum.color import Color
from linum.svg_renderer.base.style import Style


class Cell:

    def __init__(self, content: str = "", width: float = 100.0, style: Optional[Style] = None,
                 extra_classes: Optional[List[str]] = None):
        self.content = content
        self.width = width
        self.style = style or Style()

        self._extra_classes = extra_classes or []

    @property
    def height(self) -> int:
        return self.style.get("height", 100)

    @classmethod
    def get_class(cls) -> str:
        return "cell"

    def get_classes(self) -> List[str]:
        l = [self.get_class()] + self._extra_classes
        c = type(self)
        while c is not Cell:
            c = c.__bases__[0]
            l.insert(0, c.get_class())
        return l

    def _render_background(self, drawing: Drawing, x: float, y: float):
        # Style
        style = self.style.get_sub_style("background")

        # Color
        color = Color(style.get("color", 0x000000))

        # Classes
        classes = " ".join(self.get_classes() + ["background"])

        # Paddings
        padding_left = style.get("padding-left", 0)
        padding_right = style.get("padding-right", 0)
        padding_top = style.get("padding-top", 0)
        padding_bottom = style.get("padding-bottom", 0)

        # Size
        height = max(style.get("height", self.height) - padding_bottom - padding_top, 0)
        width = max(self.width - padding_left - padding_right, 0)

        # Rendering
        background = Rect(insert=(x + padding_left, y + padding_top),
                          size=(width, height),
                          class_=classes, debug=False,
                          style=style.get("style", "{}"), fill=str(color))
        drawing.add(background)
        return background

    def _render_clip_mask(self, drawing: Drawing, rect: Rect):
        # Generating id
        id_ = uuid4().hex

        # Classes
        classes = " ".join(self.get_classes() + ["clip-mask"])

        # Paddings for text item
        text_style = self.style.get_sub_style("text")
        padding_left = text_style.get("padding-left", 0)
        padding_right = text_style.get("padding-right", 0)
        padding_top = text_style.get("padding-top", 0)
        padding_bottom = text_style.get("padding-bottom", 0)

        # Size
        x = rect.attribs["x"] + padding_left
        y = rect.attribs["y"] + padding_top
        width = max(rect.attribs["width"] - padding_left - padding_right, 0)
        height = max(rect.attribs["height"] - padding_top - padding_bottom, 0)

        # Updating rect
        rect_ = rect.copy()
        rect_.update({"x": x, "y": y, "width": width, "height": height})

        # Rendering
        clip_path = ClipPath(class_=classes, id=id_)
        clip_path.add(rect_)
        drawing.add(clip_path)
        return clip_path

    def _render_text(self, drawing: Drawing, clip_path: ClipPath):
        rect = clip_path.elements[0]

        # Style
        text_style = self.style.get_sub_style("text")

        # Classes
        text_classes = " ".join(self.get_classes() + ["text"])

        # Setting text align
        align = text_style.get("align", "center")
        if align == "left":
            tx = rect.attribs["x"]
        elif align == "center":
            tx = rect.attribs["x"] + rect.attribs["width"] / 2
        elif align == "right":
            tx = rect.attribs["x"] + rect.attribs["width"]
        else:
            msg = "Incorrect align value for cell: '{}'. " \
                  "Must be 'left', 'center' or 'right'.".format(align)
            raise ValueError(msg)

        # Setting text valign
        valign = text_style.get("valign", "vcenter")
        if valign == "top":
            ty = rect.attribs["y"]
        elif valign == "vcenter":
            ty = rect.attribs["y"] + rect.attribs["height"] / 2
        elif valign == "bottom":
            ty = rect.attribs["y"] + rect.attribs["height"]
        else:
            msg = "Incorrect valign value for cell: '{}'." \
                  "Value must be 'top', 'vcenter' or 'bottom'".format(valign)
            raise ValueError(msg)

        # Text rendering
        text = Text(self.content, insert=(tx, ty), class_=text_classes, debug=False,
                    style=text_style.get("style", ""),
                    clip_path="url(#{})".format(clip_path.attribs["id"]))
        drawing.add(text)
        return text

    def _render_l_border(self, drawing: Drawing, background: Rect):
        # Style
        style = self.style.get_sub_style("border").get_sub_style("left")

        if style.get("left", False):
            # Classes
            classes = self.get_classes() + ["border"]

            # Size
            x = background.attribs["x"]
            y = background.attribs["y"]
            height = background.attribs["height"]

            # Rendering
            border = Path(["M", x, y, "L", x, y + height],
                          class_=" ".join(classes + ["left"]),
                          style=style.get("style", '{}'))
            drawing.add(border)
            return border

    def _render_r_border(self, drawing: Drawing, background: Rect):
        # Style
        style = self.style.get_sub_style("border").get_sub_style("right")

        if style.get("right", False):
            # Classes
            classes = self.get_classes() + ["border"]

            # Size
            x = background.attribs["x"] + background.attribs["width"]
            y = background.attribs["y"]
            height = background.attribs["height"]

            # Rendering
            border = Path(["M", x, y, "L", x, y + height],
                          class_=" ".join(classes + ["right"]),
                          style=style.get("style", '{}'))
            drawing.add(border)
            return border

    def _render_t_border(self, drawing: Drawing, background: Rect):
        # Style
        style = self.style.get_sub_style("border").get_sub_style("top")

        if style.get("top", False):
            # Classes
            classes = self.get_classes() + ["border"]

            # Size
            x = background.attribs["x"]
            y = background.attribs["y"]
            width = background.attribs["width"]

            # Rendering
            border = Path(["M", x, y, "L", x + width, y],
                          class_=" ".join(classes + ["top"]),
                          style=style.get("style", '{}'))
            drawing.add(border)
            return border

    def _render_b_border(self, drawing: Drawing, background: Rect):
        # Style
        style = self.style.get_sub_style("border").get_sub_style("bottom")

        if style.get("bottom", False):
            # Classes
            classes = self.get_classes() + ["border"]

            # Size
            x = background.attribs["x"]
            y = background.attribs["y"] + background.attribs["height"]
            width = background.attribs["width"]

            # Rendering
            border = Path(["M", x, y, "L", x + width, y],
                          class_=" ".join(classes + ["bottom"]),
                          style=style.get("style", '{}'))
            drawing.add(border)
            return border

    def render(self, drawing: Drawing, x: float, y: float):
        # Background
        background = self._render_background(drawing, x, y)

        # Clip mask
        clip_path = self._render_clip_mask(drawing, background)

        # Text
        self._render_text(drawing, clip_path)

        # Borders
        self._render_l_border(drawing, background)
        self._render_r_border(drawing, background)
        self._render_t_border(drawing, background)
        self._render_b_border(drawing, background)

        # drawing.save(pretty=True)  # too slow to be here
