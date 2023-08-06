from typing import Type

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.date_row import DateRow
from linum.excel_renderer.calendar.space.space_cell import SpaceCell


class SpaceRow(DateRow):

    @property
    def _date_cell_class(self) -> Type[SpaceCell]:
        return SpaceCell
