from copy import copy
from datetime import date, timedelta
from typing import Optional, Tuple

from linum.task import Task


class TaskPart:

    def __init__(self, task: Task, start_date: Optional[date] = None, length: Optional[int] = None):
        """
        Объект представления задачи или ее части.

        :param task: задача
        :param start_date: начальная дата представления
        :param length: продолжительность представления
        """
        self.task = task
        self.start = start_date or task.start_date
        self.length = task.length if length is None else length
        self.is_tail = False

    def __repr__(self):
        return "<TaskPart for '{}' starts at {} with length {}>".format(self.task.name, self.start, self.length)

    def __getitem__(self, item):
        dates = [self.start + timedelta(i) for i in range(self.length)]
        return dates[item]

    def __eq__(self, other):
        if not isinstance(other, TaskPart):
            return False
        for k, v in self.__dict__.items():
            if getattr(other, k) != v:
                return False
        return True

    def __copy__(self):
        tp = TaskPart(self.task, start_date=self.start, length=self.length)
        tp.is_tail = self.is_tail
        return tp

    def __bool__(self):
        if self.length == 0:
            return False
        return True

    @property
    def start(self) -> date:
        return self._start_date

    @start.setter
    def start(self, start_date: date):
        if start_date < self.task.start_date:
            self._start_date = self.task.start_date
        elif self.task.day_after < start_date:
            self._start_date = self.task.day_after
        else:
            self._start_date = start_date

    @property
    def length(self) -> int:
        return self._length

    @length.setter
    def length(self, length: int):
        a = self.task.day_after - self.start
        a = a.days
        b = max(length, 0)
        length = min(a, b)
        self._length = length

    @property
    def day_after(self) -> date:
        return self.start + timedelta(max(self.length, 0))

    def split(self, date_: date) -> Tuple[Optional['TaskPart'], Optional['TaskPart']]:
        """
        Функция разделения одного представления на два по заданной дате.

        Если дата разреза находится за границами текущего представления,
        то один из возвращаемых объектов будет 'None'.

        Если происходит разделение части нулевой длины, то вернется
        кортеж (TaskPart, None)

        :param date_: date
        :return: Tuple[Optional[TaskView], Optional[TaskView]]
        """
        if date_ >= self.day_after:
            return self, None

        elif date_ <= self.start:
            return None, self

        tp_after = TaskPart(self.task, date_, (self.task.day_after - date_).days)
        tp_after.is_tail = True
        tp_before = copy(self)
        tp_before.length = (date_ - self.start).days
        return tp_before, tp_after
