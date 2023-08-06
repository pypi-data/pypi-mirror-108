from datetime import date, timedelta
from typing import Optional, List

from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from linum.excel_renderer.base.style import Style
from linum.excel_renderer.calendar.space.space_row import SpaceRow
from linum.excel_renderer.calendar.views.layer_view import LayerView
from linum.layer_list import LayerList


class LayerListView:

    def __init__(self, layer_list: LayerList, start: date, length: int,
                 layer_style: Optional[Style] = None, days_off_layer_style: Optional[Style] = None,
                 days_off: Optional[List[date]] = None, workdays: Optional[List[date]] = None):
        self.layer_list = layer_list
        self.length = length
        self.start = start

        self.layer_style = layer_style or Style()
        self.days_off_layer_style = days_off_layer_style or Style()

        self.workdays = workdays
        self.days_off = days_off

        self.use_space_row = True

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook) -> int:
        # Trimming
        ll = self._trim(self.start, self.length)

        # Cleaning up
        ll.cleanup()

        offset = 1 if self.use_space_row else 0
        i = 0
        for i, layer in enumerate(ll):
            # Rendering space row before layer view
            if self.use_space_row:
                space_row_style = self.layer_style.get_sub_style("space_row").get_sub_style("_")
                days_off_space_row_style = self.days_off_layer_style.get_sub_style("space_row").get_sub_style("_")
                days_off_space_row_style.parents.insert(0, space_row_style)
                sr = SpaceRow(self.start, self.length,
                              self.days_off, self.workdays,
                              space_row_style, days_off_space_row_style)
                sr.render(row + (1 + offset) * i, column, worksheet, workbook)

            # Rendering layer view
            lv = LayerView(layer, self.start, self.length,
                           self.layer_style, self.days_off_layer_style,
                           self.days_off, self.workdays)
            lv.render(row + (1 + offset) * i + 1, column, worksheet, workbook)

        return (1 + offset) * (i + 1)

    def _trim(self, start, length) -> LayerList:
        _, ll = self.layer_list.split(start)
        ll, _ = ll.split(start + timedelta(length))
        return ll
