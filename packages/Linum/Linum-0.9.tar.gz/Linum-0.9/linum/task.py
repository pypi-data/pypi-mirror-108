from datetime import date, timedelta
from typing import Optional

from linum.color import Color


class Task:

    def __init__(self, name: str = '', start_date: date = date.today(), length: int = 1, color: Optional[int] = None):
        """
        Класс задачи.

        :param name: название задачи
        :param start_date: начальная дата
        :param length: продолжительность
        :param color: цвет задачи
        """
        self.color = color if color is not None else Color.get_random_rgb()
        self.name = name
        self.start_date = start_date
        self.length = length

    def __repr__(self):
        return "<Task '{}' starts at {}>".format(self.name, self.start_date)

    def __getitem__(self, item):
        days = [self.start_date + timedelta(i) for i in range(max(self.length, 0))]
        return days[item]

    def __eq__(self, other):
        if not isinstance(other, Task):
            return False
        return self.name == other.name \
            and self.start_date == other.start_date \
            and self.length == other.length

    def __bool__(self):
        return bool(self.length)

    def __copy__(self):
        return Task(self.name, self.start_date, self.length, self.color)

    @property
    def day_after(self) -> date:
        """
        Дата первого дня после задачи.

        :return: date
        """
        return self.start_date + timedelta(max(self.length, 0))

    @day_after.setter
    def day_after(self, date_: date):
        """
        Устанавливает длину задачи через дату после окончания задачи.

        :param date_: date
        """
        self.length = date_ - self.start_date
