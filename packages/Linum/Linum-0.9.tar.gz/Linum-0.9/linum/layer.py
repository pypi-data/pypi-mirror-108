from copy import copy
from datetime import date
from typing import List, Tuple, Optional

from linum.exceptions import IntersectionException
from linum.task_part import TaskPart


class Layer:

    def __init__(self, parts: Optional[List[TaskPart]] = None):
        """ Слой, содержащий задачи. """
        self._parts = []
        if parts:
            for p in parts:
                self.append(p)

    def __repr__(self):
        return "<Layer with {} TaskParts>".format(len(self._parts))

    def __getitem__(self, item):
        days = set()
        for v in self._parts:
            days.update(set(v[:]))
        days = sorted(days)
        return days[item]

    def __eq__(self, other):
        if not isinstance(other, Layer):
            return None
        return self.parts == other.parts

    def __copy__(self):
        layer = Layer()
        for p in self.parts:
            layer._parts.append(copy(p))
        return layer

    def __bool__(self):
        if not self.parts:
            return False
        for part in self.parts:
            if part:
                return True
        return False

    @property
    def parts(self) -> List[TaskPart]:
        return sorted(self._parts, key=lambda p: p.start)

    def check(self):
        """
        Функция проверки содержащихся кусочков задач на пересечение.
        Если пересечение есть то вызовется исключение 'IntersectionException'.

        :exception IntersectionException
        """
        d = set()
        for part in self.parts:
            s = set(part[:])
            if d.intersection(s):
                raise IntersectionException(self, part)
            d.update(s)

    def append(self, task_part: TaskPart):
        """
        Безопасное добавление части задачи на слой.
        Если есть пересечения с присутствующими частями,
        то поднимется исключение 'IntersectionException'.

        Если тип добавляемого объекта отличен от 'TaskPart',
        то добавления не происходит.

        :param task_part: добавляемая часть задачи
        :exception IntersectionException
        """
        if not isinstance(task_part, TaskPart):
            return
        days = set(self[:])
        if days.intersection(set(task_part[:])):
            raise IntersectionException(self, task_part)
        else:
            self._parts.append(task_part)

    def split(self, date_: date) -> Tuple['Layer', 'Layer']:
        """
        Функция разделения слоя на два относительно заданной даты.
        Всегда возвращает два слоя.

        Возвращаемый слой может быть и пустым.

        :param date_: дата разделения
        """
        layer_before = Layer()
        layer_after = Layer()

        for part in self._parts:
            tp_before, tp_after = part.split(date_)
            layer_before.append(tp_before)
            layer_after.append(tp_after)

        return layer_before, layer_after
