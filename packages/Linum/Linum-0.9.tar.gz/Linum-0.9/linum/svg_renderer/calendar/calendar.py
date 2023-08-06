from datetime import timedelta

from svgwrite import Drawing
from svgwrite.container import Style as CssStyle

from linum.context import SvgRendererContext
from linum.helper import split_by_months
from linum.layer_list import LayerList
from linum.svg_renderer.calendar.header.header import Header
from linum.svg_renderer.calendar.views.days_off_view import DaysOffView
from linum.svg_renderer.calendar.views.grid_view import GridView
from linum.svg_renderer.calendar.views.layer_list_view import LayerListView


class Calendar:

    def __init__(self, layer_list: LayerList, context: SvgRendererContext):
        self.context = context
        self.layer_list = layer_list

    def render(self, drawing: Drawing, x: int, y: int):
        days_off = self.context.days_off
        workdays = self.context.workdays

        # Adding css
        if self.context.css:
            css = open(self.context.css, mode="rt", encoding="utf-8").read()
            drawing.defs.add(CssStyle(css))
            drawing.save(pretty=True)

        # Preparing styles
        styles = self.context.styles
        header_style = styles.get_sub_style("header")
        tasks_style = styles.get_sub_style("layers").get_sub_style("tasks")

        # Splitting by periods
        y_ = y
        months = split_by_months(self.context.start, self.context.length)
        for i in range(0, len(months), self.context.months_in_row):
            m = months[i:i + self.context.months_in_row]
            d, _ = m[0]
            length = sum([d for _, d in m])

            _, layer_list = self.layer_list.split(d)
            layer_list, _ = self.layer_list.split(d + timedelta(length))
            layer_list.cleanup()

            # Rendering header
            header = Header(d, length, self.context.width, header_style)
            header.render(drawing, x, y_)

            # Rendering layer list
            llv = LayerListView(layer_list, d, length, self.context.width, tasks_style)
            llv.render(drawing, x, y_ + header.height)

            # Rendering days-off
            dov = DaysOffView(len(llv.layer_list.layers), d, length, self.context.width,
                              styles, workdays, days_off)
            dov.render(drawing, x, y_)

            # Rendering grid
            gv = GridView(len(llv.layer_list.layers), d, length,
                          self.context.width, styles)
            gv.render(drawing, x, y_)

            # Calculating offset
            indent = styles.get_sub_style("layers").get("indent", 24)
            y_ += header.height + llv.height + indent

        drawing["width"] = "{}px".format(self.context.width)
        drawing["height"] = "{}px".format(y_)

        drawing.save(pretty=True)
