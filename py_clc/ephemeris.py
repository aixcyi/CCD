import math
from collections import OrderedDict
from datetime import date, timedelta, datetime, time
from typing import NoReturn, NamedTuple

import ephem

from py_clc.base import (
    FastCCD,
    _check_date_fields as _check_fields,
)

DELTA = timedelta(hours=8)  # 零时区和东八区的时差


class Month(NamedTuple):
    ords: int
    is_leap: bool

    @classmethod
    def fromtuple(cls, t: tuple):
        return cls(*t)


class MonthInfo(NamedTuple):
    start: date  # 东八区下的日期
    days: int


def _calc(_time, epoch) -> ephem.Angle:
    """
    求太阳某个时刻的地心视黄经。
    """
    sun = ephem.Sun(_time)
    equ = ephem.Equatorial(sun.ra, sun.dec, epoch=epoch)
    ecl = ephem.Ecliptic(equ)
    return abs(ecl.lon.norm / math.pi * 180)  # [0,2*pi)


def _check_if_leap(prev_date: date,
                   next_date: date,
                   epoch: ephem.Date) -> bool:
    """
    判断两个朔日之间是否没有中气。
    """
    # UTC+8 转 UTC+0，并将时间拨到 上个朔日当天第一秒，下个朔日的前一天最后一秒
    pt = datetime.combine(prev_date, time()) - DELTA
    nt = datetime.combine(next_date, time()) - DELTA - timedelta(seconds=1)

    # 计算地心视黄经
    pr = _calc(pt, epoch=epoch)
    nr = _calc(nt, epoch=epoch)
    nr = nr if pr <= nr else (360 + nr)

    # 地心视黄经为 0° 或 30° 的整数倍时，那一天即为中气
    pd, pm = divmod(pr, 30)
    nd, nm = divmod(nr, 30)
    return pd == nd and pm != 0 != nm


def _enum_months(year: int) -> OrderedDict[Month, MonthInfo]:
    """
    枚举公历年去年冬至所在月份（农历十一月）至
    公历当年冬至前一个月份（农历十月/闰十月）之间的所有农历月。
    """
    # 获取去年和今年的冬至（Winter Solstice）
    pws = ephem.previous_solstice(str(year))
    nws = ephem.previous_solstice(str(year + 1))

    # 求出每个月的初一（从去年冬至前的朔日到今年冬至前的朔日）
    starts: list[date] = []
    start: ephem.Date = ephem.previous_new_moon(pws)
    while start < nws:
        starts.append((start.datetime() + DELTA).date())  # 转换为东八区当天凌晨零点
        start = ephem.next_new_moon(start)

    mos = (11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)  # (month-ordinal)s
    tags = (False,) * 12  # (is_leap_month)s

    # 合朔12次则不置闰
    if (times := len(starts) - 1) == 12:
        return OrderedDict(
            (
                Month(mos[i], False),
                MonthInfo(starts[i], (starts[i + 1] - starts[i]).days)
            )
            for i in range(times)
        )

    # 合朔超过12次，闰月为冬至所在月开始的第一个无中气月
    for i in range(times):
        cs = starts[i]
        ns = starts[i + 1]
        if _check_if_leap(cs, ns, epoch=pws):
            vals = (
                MonthInfo(cs, (ns - cs).days)
                for i in range(times)
            )
            keys = map(Month.fromtuple, zip(
                mos[:i] + (mos[i - 1],) + mos[i:],
                tags[:i] + (True,) + tags[i:],
            ))
            return OrderedDict(zip(keys, vals))
    raise RuntimeError(f'合朔超过十二次但没有找到 {year} 年的闰月。')


def _get_months(year: int):
    """
    获取当前农历年的所有月份。
    """
    _curr = _enum_months(year)
    _next = _enum_months(year + 1)
    _curr.popitem(last=False)
    _curr.popitem(last=False)
    _curr.update(OrderedDict(
        (_next.popitem(last=False),
         _next.popitem(last=False))
    ))
    return _curr


def _check_date_fields(y, m, d, leap) -> NoReturn:
    # 基础检查
    _check_fields(y, m, d, leap)
    # 岁首在十一月，所以如果提供的农历月在十一月之后，就需要枚举下一个农历年的农历月。
    months = _enum_months(y if m < 11 else (y + 1))
    prefix = '闰' if leap else ''
    if (_month := Month(m, leap)) not in months:
        raise ValueError(
            f'农历 {y}年 没有 {prefix}{m}月。'
        )
    if not d <= months[_month].days:
        raise ValueError(
            f'农历 {y}年 {prefix}{m}月 没有 {d} 日。'
        )


class ChineseCalendarDate(FastCCD):

    def __new__(cls, year, month=1, day=1, is_leap_month: bool = False):
        _check_date_fields(year, month, day, is_leap_month)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._leap = is_leap_month
        self._hashcode = -1
        return self

    @classmethod
    def from_date(cls, _date: date) -> 'ChineseCalendarDate':
        if not isinstance(_date, date):
            raise TypeError(
                '只接受 datetime.date 及其衍生类型的公历日期。'
            )
        solstice = ephem.previous_solstice(str(_date.year)).datetime().date()
        months = _enum_months(_date.year if solstice <= _date else (_date.year - 1))
        last_moon = None
        last_info = None
        for m in months:
            if months[m].start == _date:
                return cls(_date.year, m.ords, 1, m.is_leap)
            elif months[m].start < _date:
                last_moon = m
                last_info = months[m]
            else:
                day = (_date - last_info.start).days + 1
                return cls(_date.year, last_moon.ords, day, last_moon.is_leap)

    @classmethod
    def from_ordinal(cls, n) -> 'ChineseCalendarDate':
        return cls.from_date(date.fromordinal(n))

    fromordinal = from_ordinal

    # 只读属性

    @property
    def days_in_year(self) -> int:
        months = _get_months(self._year)
        return sum(months[month].days for month in months)

    @property
    def days_in_month(self) -> int:
        months = _get_months(self._year)
        return months[Month(self._month, self._leap)].days

    @property
    def day_of_year(self) -> int:
        months = _get_months(self._year)
        _month = Month(self._month, self._leap)
        return sum(info.days for m, info in months.items() if m < _month) + self._day

    # 计算方法

    def __add__(self, other):
        if isinstance(other, timedelta):
            if (days := other.days) == 0:
                return self.replace()
            if days < 0:
                return self.__sub__(-other)
            n = self.to_ordinal() + days
            return self.from_ordinal(n)
        raise NotImplementedError

    __radd__ = __add__

    def __sub__(self, other):
        if isinstance(other, timedelta):
            if (days := other.days) == 0:
                return self.replace()
            if days < 0:
                return self.__add__(-other)
            n = self.to_ordinal() - days
            assert 0 < n
            return self.from_ordinal(n)
        elif isinstance(other, FastCCD):
            n = self.to_ordinal() - other.to_ordinal()
            assert 0 < n
            return self.from_ordinal(n)
        raise NotImplementedError

    # 转换器

    def to_date(self) -> date:
        months = _enum_months(self._year - (0 if self._month < 11 else 1))
        start = months[Month(self._month, self._leap)].start
        return start + timedelta(days=self._day - 1)

    def to_ordinal(self) -> int:
        return self.to_date().toordinal()

    toordinal = to_ordinal


EphemCCD = ChineseCalendarDate
