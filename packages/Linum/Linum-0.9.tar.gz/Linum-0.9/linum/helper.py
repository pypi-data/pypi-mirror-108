import colorsys
from datetime import timedelta, date
from typing import List, Tuple, Optional

from linum.txt_renderer.enums import Align


def days_in_month(date_: date.today()) -> int:
    """
    Returns days count in specified month

    :param date_: date of month
    :return: int
    """
    year = date_.year
    month = date_.month
    next_month = month + 1 if month + 1 < 13 else 1
    d = date(year=year, month=next_month, day=1)
    last_day_in_month = d - timedelta(days=1)
    return last_day_in_month.day


def split_by_months(start_date: date, length: int) -> List[Tuple[date, int]]:
    """
    Разделяет указанный период по месяцам.
    Возвращает список с кортежами - по одному на месяц.
    Каждый кортеж представляет из себя начальную дату месяца
    и количество дней в месяце.
    Если заданный период начинается не с начала месяца,
    то соответствующий кортеж будет указывать на заданную начальную дату
    и количество дней до конца месяца.

    :param start_date: начальная дата анализируемого периода
    :param length: продолжительность периода
    :rtype: List[Tuple[date, int]]
    """
    if length <= 0:
        return [(start_date, 0)]

    # Получаем список всех дат периода
    dates = [start_date + timedelta(i) for i in range(length)]

    months = []
    previous = 0
    # Разделяем список дат на месяцы
    for i in range(len(dates)):
        if dates[i].day == 1:
            months.append(dates[previous: i])
            previous = i
    # Добавляем последний промежуток
    months.append(dates[previous:])

    # Корректируем список
    if start_date.day == 1:
        months.pop(0)

    result = []
    # Формируем результат
    for month in months:
        result.append((month[0], len(month)))

    return result


def supp_content(content: str, length: int, align: Align = Align.LEFT, fill_char: str = ' ') -> str:
    """
    Дополняет строку до указанной длины символами `fill_char`.

    :param content: содержимое для выравнивания
    :param length: требуемая длина
    :param align: выравнивание
    :param fill_char: символ заполнения
    :return: str
    """
    if len(content) >= length:
        return content

    # Дополняем символами справа
    if align is Align.LEFT:
        while len(content) < length:
            content += str(fill_char)

    # Дополняем символами слева
    elif align is Align.RIGHT:
        while len(content) < length:
            content = str(fill_char) + content

    # Дополняем символами с обеих сторон
    elif align is Align.CENTER:
        position = int(length / 2 - len(content) / 2)
        prefix = str(fill_char) * position
        postfix = str(fill_char) * (length - len(prefix) - len(content))
        content = prefix + content + postfix
    return content


def trim_content(content: str, length: int) -> str:
    """
    Trims content to specified length.

    :param content: content to trim
    :param length: specified length
    :return: str
    """
    if length <= 0:
        return ''
    if len(content) > length:
        return content[:length - 1] + "…"
    return content


def rgb_to_hsv(rgb: int) -> Tuple[float, float, float]:
    """
    Converts rgb int value to hue, saturation and value parts in percents.

    :param rgb: int value
    :return: Tuple[float, float, float]
    """
    r = (rgb & 0xFF0000) >> 16
    g = (rgb & 0x00FF00) >> 8
    b = rgb & 0x0000FF

    r, g, b = r / 255, g / 255, b / 255

    return colorsys.rgb_to_hsv(r, g, b)


def hsv_to_rgb(h: float, s: float, v: float) -> int:
    """
    Converts hue, saturation and value parts in percents to rgb int value.

    :param h: hue part in percents
    :param s: saturation part in percents
    :param v: value part in percents
    :return: int
    """
    r, g, b = colorsys.hsv_to_rgb(h, s, v)

    r, g, b, = int(r * 255), int(g * 255), int(b * 255)

    r = r << 16
    g = g << 8

    return r + g + b


def add_blackout(rgb, blackout: float) -> int:
    """
    Adds blackout to specified rgb color

    :param rgb: rgb color as int
    :param blackout: blackout value as percents
    :return: rgb as int
    """
    h, s, v = rgb_to_hsv(rgb)
    v = max(0.0, v - blackout)
    rgb = hsv_to_rgb(h, s, v)
    return rgb


def color_to_str(rgb: int) -> str:
    if isinstance(rgb, str):
        return rgb
    return '#' + hex(rgb)[2:].zfill(6)


def is_day_off(date_: date, days_off: Optional[List[date]] = None, workdays: Optional[List[date]] = None) -> bool:
    days_off = days_off or []
    workdays = workdays or []
    day_off = date_.weekday() == 5 or date_.weekday() == 6
    day_off = day_off or date_ in days_off
    day_off = day_off and date_ not in workdays
    return day_off
