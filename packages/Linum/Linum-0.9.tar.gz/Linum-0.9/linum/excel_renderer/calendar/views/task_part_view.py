from datetime import date
from typing import Optional, List

from linum.excel_renderer.base.date_cell import DateCell
from linum.excel_renderer.base.style import Style
from linum.excel_renderer.calendar.space.space_row import SpaceRow
from linum.task_part import TaskPart


class TaskPartView(SpaceRow):

    def __init__(self, task_part: TaskPart,
                 days_off: Optional[List[date]] = None, workdays: Optional[List[date]] = None,
                 workday_style: Optional[Style] = None, days_off_style: Optional[Style] = None):
        super().__init__(task_part.start, task_part.length, days_off, workdays, workday_style, days_off_style)
        self.task_part = task_part

    @property
    def cells(self) -> List[DateCell]:
        cells = super().cells
        cells[0].content = self.task_part.task.name
        return cells
