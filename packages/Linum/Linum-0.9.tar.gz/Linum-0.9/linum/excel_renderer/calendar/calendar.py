from xlsxwriter import Workbook
from xlsxwriter.worksheet import Worksheet

from linum.context import ExcelRendererContext
from linum.excel_renderer.calendar.header.header import Header
from linum.excel_renderer.calendar.space.space_row import SpaceRow
from linum.excel_renderer.calendar.views.layer_list_view import LayerListView
from linum.helper import split_by_months
from linum.layer_list import LayerList


class Calendar:

    def __init__(self, layer_list: LayerList, context: ExcelRendererContext):
        self.context = context
        self.layer_list = layer_list

    def render(self, row: int, column: int, worksheet: Worksheet, workbook: Workbook):
        days_off = self.context.days_off
        workdays = self.context.workdays

        # Base styles
        styles = self.context.styles
        days_off_styles = styles.get_sub_style("days_off")

        # Header styles
        header_style = styles.get_sub_style("header")
        days_off_header_style = days_off_styles.get_sub_style("header")

        # Layer styles
        layers_style = styles.get_sub_style("layers")
        days_off_layers_style = days_off_styles.get_sub_style("layers")

        # Space row styles
        space_row_style = layers_style.get_sub_style("space_row").get_sub_style("_")
        space_row_style.update({"bottom": 1, "bottom_color": 0xE0E0E0})
        days_off_space_row_style = days_off_layers_style.get_sub_style("space_row").get_sub_style("_")
        days_off_space_row_style.parents.insert(0, space_row_style)

        # Splitting by periods
        row_offset = 0
        months = split_by_months(self.context.start, self.context.length)
        for i in range(0, len(months), self.context.months_in_row):
            m = months[i:i + self.context.months_in_row]
            d, _ = m[0]
            days = sum([d for _, d in m])

            # Rendering header
            header = Header(d, days, days_off, workdays,
                            header_style, days_off_header_style)
            header.render(row + row_offset, column, worksheet, workbook)

            # Rendering layer list
            llv = LayerListView(self.layer_list, d, days,
                                layers_style, days_off_layers_style,
                                days_off, workdays)
            offset = llv.render(row + row_offset + 3, column, worksheet, workbook)

            # Rendering space row
            sr = SpaceRow(d, days, days_off, workdays,
                          space_row_style, days_off_space_row_style)
            sr.render(row + row_offset + 3 + offset, column, worksheet, workbook)

            # Calculating offset
            row_offset = row_offset + 3 + offset + 1
