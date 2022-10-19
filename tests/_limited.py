from datetime import date, timedelta
from random import randint

from py_clc.limited import ChineseCalendarDate
from tests.utils import BearTimer


def __speed_test__new():
    day = ChineseCalendarDate(2022, 9, 23)
    assert day

    with BearTimer('ChineseCalendarDate.__new__'):
        for _ in range(20_0000):
            _ = ChineseCalendarDate(randint(1902, 2099), randint(1, 12), randint(1, 29))


def __speed_test__from_date():
    day = date(2022, 10, 18)
    assert ChineseCalendarDate.from_date(day) == ChineseCalendarDate(2022, 9, 23)

    with BearTimer('ChineseCalendarDate.from_date'):
        for _ in range(20_0000):
            day = date(randint(1902, 2099), randint(1, 12), randint(1, 28))
            _ = ChineseCalendarDate.from_date(day)


def __speed_test__to_date():
    day = ChineseCalendarDate(2022, 9, 23)
    assert day.to_date() == date(2022, 10, 18)

    with BearTimer('ChineseCalendarDate.to_date'):
        for _ in range(20_0000):
            day = ChineseCalendarDate(randint(1902, 2099), randint(1, 12), randint(1, 29))
            _ = day.to_date()


def __speed_test__add():
    day = ChineseCalendarDate(2022, 9, 23)
    assert day.to_date() == date(2022, 10, 18)

    with BearTimer('ChineseCalendarDate.to_date'):
        today = ChineseCalendarDate(2022, 10, 17)
        for _ in range(2_0000):
            _ = today + timedelta(days=randint(0, 600))
    with BearTimer('ChineseCalendarDate.to_date'):
        today = date(2022, 10, 17)
        for _ in range(80_0000):
            _ = today + timedelta(days=randint(0, 600))


if __name__ == '__main__':
    __speed_test__new()
    __speed_test__from_date()
    __speed_test__to_date()
    __speed_test__add()
