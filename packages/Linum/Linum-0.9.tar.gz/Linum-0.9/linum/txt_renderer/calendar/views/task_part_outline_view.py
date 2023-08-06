from linum.task_part import TaskPart
from linum.txt_renderer.base.border import Border
from linum.txt_renderer.base.cell import Cell
from linum.txt_renderer.base.date_row import DateRow
from linum.txt_renderer.calendar.grid.grid_row import GridRow


class TaskPartOutlineView(DateRow):

    def __init__(self, task_part: TaskPart):
        """
        Представление кусочка задачи.

        :param task_part: кусочек задачи
        """
        self.task_part = task_part
        super().__init__(task_part.start, task_part.length)

    def pre_render(self, is_top_outline=True) -> Cell:
        """
        Возвращает строковое представление верхнего или нижнего сегмента кусочка задачи.

        :param is_top_outline: верхняя или нижняя часть
        :return: Cell
        """
        gr = GridRow(self.start_date, self.length, is_top_outline)
        gr.cell_width = self.cell_width
        gr.inner_borders = self.inner_borders
        gr.month_inner_borders = self.month_inner_borders
        gr.left_border = True
        gr.right_border = True
        cell = gr.merge()
        if self.inner_borders:
            cell.left_border_char += Border(t=is_top_outline, b=not is_top_outline)
            cell.right_border_char += Border(t=is_top_outline, b=not is_top_outline)
        if not self.inner_borders:
            cell.content = cell.content[1:-1]
            cell.cell_width -= 2
            content = cell.render()
            cell = Cell(len(content), content)

        return cell
