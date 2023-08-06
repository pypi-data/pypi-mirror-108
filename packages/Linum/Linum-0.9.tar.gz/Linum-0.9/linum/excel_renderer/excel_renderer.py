from datetime import datetime
from typing import Optional

import xlsxwriter

from linum.composer import Composer
from linum.excel_renderer.calendar.calendar import Calendar
from linum.loader import Loader


class ExcelRenderer:

    def __init__(self, tasks_path: str, context_path: Optional[str] = '', out_path: Optional[str] = ''):
        self.tasks_path = tasks_path
        self.context_path = context_path
        self.out_path = out_path

    def render(self):
        # Loading tasks
        tasks = Loader().load_tasks(self.tasks_path)

        # Getting layer list
        layer_list = Composer(tasks).safety_compose()

        # Loading context
        if self.context_path:
            context = Loader.load_excel_renderer_context(self.context_path)
        else:
            context = Loader.load_default_xlsx_context()

        # Calculating name of output file
        path = self.out_path or self.get_default_file_name()

        # Pre render
        workbook = xlsxwriter.Workbook(path)
        worksheet = workbook.add_worksheet('Linum')

        # Rendering
        c = Calendar(layer_list, context)
        c.render(1, 1, worksheet, workbook)
        workbook.close()

    @staticmethod
    def get_default_file_name() -> str:
        d = datetime.now()
        s = "Linum {}.xlsx".format(d.strftime("%Y-%m-%d %H.%M"))
        return s
