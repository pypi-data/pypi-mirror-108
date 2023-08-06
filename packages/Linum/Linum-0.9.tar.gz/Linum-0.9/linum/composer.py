from typing import List, Optional

from linum.layer_list import LayerList
from linum.task import Task
from linum.task_part import TaskPart


class Composer:

    def __init__(self, tasks: Optional[List[Task]] = None):
        """
        Компоновщик задач в слои.

        :param tasks: компонуемые задачи
        """
        self.tasks = tasks or []

    def safety_compose(self) -> LayerList:
        """
        Компоновщик, исключающий пересечения задач.

        :return:
        """
        layer_list = LayerList()
        for task in self.tasks:
            layer_list.add_task_part(TaskPart(task))
        return layer_list
