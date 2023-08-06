from datetime import datetime
from typing import Optional

from linum.composer import Composer
from linum.context import TxtRendererContext
from linum.loader import Loader
from linum.txt_renderer.calendar.calendar import Calendar


class TxtRenderer:

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
            context = Loader.load_txt_renderer_context(self.context_path)
        else:
            context = TxtRendererContext()

        # Calculating name of output file
        path = self.out_path or self.get_default_file_name()

        # Rendering
        c = Calendar(layer_list, context)
        file = open(path, mode="wt", encoding="utf-8")
        file.write(c.render())
        file.close()

    @staticmethod
    def get_default_file_name() -> str:
        d = datetime.now()
        s = "Linum {}.txt".format(d.strftime("%Y-%m-%d %H.%M"))
        return s
