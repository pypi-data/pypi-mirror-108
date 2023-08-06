from datetime import date
from typing import Optional, List

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.style import Style
from linum.excel_renderer.calendar.space.space_row import SpaceRow
from linum.excel_renderer.calendar.views.task_part_view import TaskPartView
from linum.layer import Layer


class LayerView:

    def __init__(self, layer: Layer, start: date, length: int,
                 layer_style: Optional[Style] = None, days_off_layer_style: Optional[Style] = None,
                 days_off: Optional[List[date]] = None, workdays: Optional[List[date]] = None):
        self.length = length
        self.start = start
        self.layer = layer

        self.layer_style = layer_style or Style()
        self.days_off_layer_style = days_off_layer_style or Style()

        self.workdays = workdays
        self.days_off = days_off

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook):
        # Rendering empty space
        space_style = self.layer_style.get_sub_style("space")
        days_off_space_style = self.days_off_layer_style.get_sub_style("space")
        days_off_space_style.parents.insert(0, space_style)
        sr = SpaceRow(self.start, self.length,
                      self.days_off, self.workdays,
                      space_style, days_off_space_style)
        sr.render(row, column, worksheet, workbook)

        # Rendering task parts
        for part in self.layer.parts:
            # Base style to apply
            base_style = Style(debug_name="base_style", bg_color=part.task.color)

            task_part_style = self.layer_style.get_sub_style("tasks").get_sub_style("_")
            task_part_style.parents.append(base_style)

            days_off_task_part_style = self.days_off_layer_style.get_sub_style("tasks").get_sub_style("_")
            days_off_task_part_style.parents.insert(0, task_part_style)

            tpv = TaskPartView(part, self.days_off, self.workdays, task_part_style, days_off_task_part_style)
            tpv.render(row, (part.start - self.start).days + column, worksheet, workbook)

