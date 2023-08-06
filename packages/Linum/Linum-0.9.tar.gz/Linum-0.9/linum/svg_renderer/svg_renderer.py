import locale
from datetime import datetime
from typing import Optional

from svgwrite import Drawing

from linum.composer import Composer
from linum.loader import Loader
from linum.svg_renderer.calendar.calendar import Calendar


class SvgRenderer:

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
            context = Loader.load_svg_renderer_context(self.context_path)
        else:
            context = Loader.load_default_svg_context()

        # Setting locale
        prev_locale = locale.getlocale(locale.LC_TIME)
        if context.locale:
            locale.setlocale(locale.LC_TIME, context.locale)

        # Calculating name of output file
        path = self.out_path or self.get_default_file_name()

        # Preparing drawing
        dwg = Drawing(filename=path, profile="full")

        # Rendering
        calendar = Calendar(layer_list, context)
        calendar.render(dwg, 0, 0)

        # Unsetting locale
        if context.locale:
            locale.setlocale(locale.LC_TIME, prev_locale)

    @staticmethod
    def get_default_file_name() -> str:
        d = datetime.now()
        s = "Linum {}.svg".format(d.strftime("%Y-%m-%d %H.%M"))
        return s
