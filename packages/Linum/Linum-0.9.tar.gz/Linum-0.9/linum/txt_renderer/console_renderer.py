from typing import Optional

from linum.composer import Composer
from linum.context import TxtRendererContext
from linum.loader import Loader
from linum.txt_renderer.calendar.calendar import Calendar


class ConsoleRenderer:

    def __init__(self, tasks_path: str, context_path: Optional[str] = ''):
        self.tasks_path = tasks_path
        self.context_path = context_path

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

        # Rendering
        c = Calendar(layer_list, context)
        print(c.render())
