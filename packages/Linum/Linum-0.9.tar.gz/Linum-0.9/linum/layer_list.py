from datetime import date
from typing import List, Tuple, Optional

from linum.exceptions import IntersectionException
from linum.layer import Layer
from linum.task_part import TaskPart


class LayerList:

    def __init__(self, layers: Optional[List[Layer]] = None):
        """
        Массив слоев.

        :param layers: слои для добавления в список
        """
        self.layers = layers or []

    def __repr__(self):
        return "<LayerList with {} layer(s)>".format(len(self.layers))

    def __eq__(self, other):
        if not isinstance(other, LayerList):
            return False
        return self.layers == other.layers

    def __getitem__(self, item):
        return self.layers[item]

    def __bool__(self):
        if not self.layers:
            return False
        for layer in self.layers:
            if layer:
                return True
        return False

    def split(self, split_date: date) -> Tuple['LayerList', 'LayerList']:
        """
        Функция разделения списка слоев на два относительно указанной даты.

        :param split_date: date
        :return:
        """
        list_before = LayerList()
        list_after = LayerList()

        for layer in self.layers:
            layer_before, layer_after = layer.split(split_date)
            list_before.layers.append(layer_before)
            list_after.layers.append(layer_after)

        return list_before, list_after

    def add_task_part(self, task_part: TaskPart):
        """
        Добавление кусочка задачи в список слоев.
        Если есть свободное место в текущих слоях, то кусочек добавится к ним.
        Если свободного места нет, то список слоев расширится на один слой и
        кусочек задачи будет помещен на этот новый слой.

        :param task_part: кусочек задачи для добавления
        """
        for layer in self.layers:
            try:
                layer.append(task_part)
                return
            except IntersectionException:
                pass
        layer = Layer([task_part])
        self.layers.append(layer)

    def cleanup(self):
        layers = []
        for layer in self.layers:
            if layer:
                layers.append(layer)
        self.layers = layers
