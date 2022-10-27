from datetime import date, timedelta
from random import randint

from py_clc.limited import ChineseCalendarDate, CCD_ORDINAL_MIN, CCD_ORDINAL_MAX
from tests.utils import BearTimer


def __speed_test__new():
    ccd = ChineseCalendarDate(2022, 9, 23)
    assert ccd.year == 2022 and ccd.month == 9 and ccd.day == 23

    with BearTimer('ChineseCalendarDate.__new__'):
        for _ in range(20_0000):
            ChineseCalendarDate(
                randint(1902, 2099), randint(1, 12), randint(1, 28)
            )
    with BearTimer('datetime.date.__new__'):
        for _ in range(20_0000):
            ChineseCalendarDate(
                randint(1902, 2099), randint(1, 12), randint(1, 28)
            )


def __speed_test__from_date():
    day = date(2022, 10, 18)
    ccd = ChineseCalendarDate.from_date(day)
    assert ccd.year == 2022 and ccd.month == 9 and ccd.day == 23

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


def __speed_test__fromordinal():
    ccd = ChineseCalendarDate.fromordinal(44467)
    assert ccd.year == 2022 and ccd.month == 9 and ccd.day == 23

    with BearTimer('ChineseCalendarDate.fromordinal'):
        for _ in range(20_0000):
            n = randint(CCD_ORDINAL_MIN, CCD_ORDINAL_MAX)
            ChineseCalendarDate.fromordinal(n)


def __speed_test__toordinal():
    day = ChineseCalendarDate(2022, 9, 23)
    assert day.toordinal() == 44467

    with BearTimer('ChineseCalendarDate.toordinal'):
        for _ in range(20_0000):
            day = ChineseCalendarDate(randint(1902, 2099), randint(1, 12), randint(1, 29))
            _ = day.toordinal()


def __speed_test__str():
    ccd = ChineseCalendarDate(2022, 9, 23)
    assert str(ccd) == '农历2022年九月廿三'

    with BearTimer('ChineseCalendarDate.__str__'):
        for _ in range(20_0000):
            day = ChineseCalendarDate(randint(1902, 2099), randint(1, 12), randint(1, 29))
            _ = str(day)

    with BearTimer('datetime.date.__str__'):
        for _ in range(20_0000):
            day = date(randint(1902, 2099), randint(1, 12), randint(1, 28))
            _ = str(day)


def __speed_test__add():
    ccd = ChineseCalendarDate(2022, 9, 23) + timedelta(days=1)
    assert ccd.year == 2022 and ccd.month == 9 and ccd.day == 24
    ccd = ChineseCalendarDate(2022, 9, 23) + timedelta(days=21)
    assert ccd.year == 2022 and ccd.month == 10 and ccd.day == 15

    with BearTimer('ChineseCalendarDate.__add__'):
        today = ChineseCalendarDate(2022, 10, 17)
        for _ in range(20_0000):
            _ = today + timedelta(days=randint(0, 20000))
    with BearTimer('datetime.date.__add__'):
        today = date(2022, 10, 17)
        for _ in range(20_0000):
            _ = today + timedelta(days=randint(0, 20000))


if __name__ == '__main__':
    __speed_test__new()
    __speed_test__from_date()
    __speed_test__to_date()
    __speed_test__fromordinal()
    __speed_test__toordinal()
    __speed_test__add()
    __speed_test__str()
