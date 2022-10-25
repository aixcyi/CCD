import math
from collections import OrderedDict
from datetime import date, timedelta, datetime
from typing import NoReturn

import ephem

from py_clc.base import ChineseCalendarDate as _Date


def r2d(rad) -> float:
    """
    弧度（radian）转角度（degrees）。
    """
    if isinstance(rad, ephem.Angle):
        return rad.norm / math.pi * 180  # [0,2*pi)
    else:
        return rad / math.pi * 180


def calc(_time, epoch) -> ephem.Angle:
    """
    求太阳某个时刻的地心视黄经。
    """
    sun = ephem.Sun(_time)
    equ = ephem.Equatorial(sun.ra, sun.dec, epoch=epoch)
    ecl = ephem.Ecliptic(equ)
    return ecl.lon


def reset(_time: datetime) -> datetime:
    """
    略去 datetime 中的 time，只保留 date 部分。
    """
    return _time.replace(hour=0, minute=0, second=0, microsecond=0)


def _check_if_leap(prev_new_moon: datetime, next_new_moon: datetime, epoch) -> bool:
    """
    判断从上个朔日当天到下个朔日之前的时间段内是否有中气。
    """
    # 将时间修正到：上个朔日当天第一秒，下个朔日的前一天最后一秒
    prev_time = reset(prev_new_moon)
    next_time = reset(next_new_moon) - timedelta(seconds=1)

    # 涉及计算的，必须将 UTC+8 时间转回 UTC+0 时间
    prev_lon = abs(r2d(calc(prev_time - timedelta(hours=8), epoch=epoch)))
    next_lon = abs(r2d(calc(next_time - timedelta(hours=8), epoch=epoch)))

    # 如果度数从 270° 一侧跨越 0° 到 90° 一侧，就会满足这个条件，
    # 那么 +360° 改为 prev_lon < next_lon 更方便判断。
    # 如果没有跨越，那么一定是 prev_lon < next_lon
    if prev_lon > next_lon:
        next_lon += 360
    # print(prev_time, next_time, prev_lon, next_lon, sep='   \t')

    # 到达中气的时候，地心视黄经是 0° ，或者是 30° 的整数倍。
    # 因此如果两个月初时刻的地心视黄经之间有 0° ，或者 30° 的整数倍，
    # 那么这个月就有中气，反之则表示没有。
    # 自岁首（十一月）开始的第一个无中气月是闰月，后续直至岁末（十月/闰十月）都不再置闰。
    for angle in range(0, 720, 30):
        if prev_lon <= angle <= next_lon:
            return False
    return True


def _enum_months(_year: int) -> OrderedDict[tuple[int, bool], tuple[int, date]]:
    """
    枚举公历年去年冬至所在月份（农历十一月）至
    公历当年冬至前一个月份（农历十月/闰十月）之间的所有农历月。
    """
    # 获取去年十一月到今年十一月的朔日（两端点是包含冬至的月份，所以必定不是闰十一月）。
    # 农历以北京时间为准，所以需要将 UTC+0 时间转换为 UTC+8 时间。
    prev = ephem.previous_solstice(str(_year))
    curr = ephem.previous_solstice(str(_year + 1))
    days = [ephem.previous_new_moon(prev).datetime() + timedelta(hours=8)]
    day = prev
    day = ephem.next_new_moon(day)
    while day <= curr:
        days.append(day.datetime() + timedelta(hours=8))
        day = ephem.next_new_moon(day)

    mos = (11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)  # (month-ordinal)s
    tags = (False,) * 12  # (is_leap_month)s

    # 最后一次合朔在农历今年十一月的，不在同一个统计周期，故减去。
    # 合朔12次则不置闰，所有月份都是非闰月。
    if (times := len(days) - 1) == 12:
        days = tuple(_d.date() for _d in days)
        keys = ((_m, False) for _m in mos)
        vals = (
            ((days[i + 1] - days[i]).days, days[i])
            for i in range(len(days) - 1)
        )
        return OrderedDict(zip(keys, vals))

    # 合朔超过12次则需要置闰，闰月为自岁首(十一月)开始的第一个无中气月。
    for i in range(times):
        if _check_if_leap(days[i], days[i + 1], epoch=prev):
            days = tuple(_d.date() for _d in days)
            keys = zip(
                mos[:i] + (mos[i - 1],) + mos[i:],
                tags[:i] + (True,) + tags[i:]
            )
            vals = (
                ((days[i + 1] - days[i]).days, days[i])
                for i in range(len(days) - 1)
            )
            return OrderedDict(zip(keys, vals))
    raise RuntimeError(f'合朔超过十二次但没有找到 {_year} 年的闰月。')


class ChineseCalendarDate(_Date):

    def __new__(cls, year: int, month=1, day=1, is_leap_month: bool = False):
        cls._check_date_fields(year, month, day, is_leap_month)
        self = _Date.__new__(cls, year, month, day, is_leap_month)
        return self

    # 静态方法 ================================

    @classmethod
    def _check_date_fields(cls,
                           year: int,
                           month: int,
                           day: int,
                           is_leap_month: bool) -> NoReturn:
        super()._check_date_fields(
            year, month, day, is_leap_month
        )
        # 岁首在十一月，所以如果提供的农历月在十一月之后，就需要枚举下一个农历年的农历月。
        months = _enum_months(year if month < 11 else (year + 1))

        if (_month := (month, is_leap_month)) not in months:
            prefix = '闰' if is_leap_month else ''
            raise ValueError(f'农历{year}年没有{prefix}{month}月。')
        if not day <= months[_month][0]:
            raise ValueError(f'提供的农历日 {day} 超过了当月日期范围。')

    # 只读属性 ================================

    @staticmethod
    def months(_year: int):
        _curr = _enum_months(_year)
        _next = _enum_months(_year + 1)
        _curr.popitem(last=False)
        _curr.popitem(last=False)
        _curr.update(OrderedDict(
            (_next.popitem(last=False),
             _next.popitem(last=False))
        ))
        return _curr

    @property
    def days_in_year(self) -> int:
        months = self.months(self._year)
        return sum(months[month][0] for month in months)

    @property
    def days_in_month(self) -> int:
        months = self.months(self._year)
        return months[(self._month, self._leap)][0]

    @property
    def day_of_year(self) -> int:
        months = self.months(self._year)
        _month = (self._month, self._leap)
        return sum(days for m, days in months.items() if m < _month) + self._day

    # 历法推算 ================================

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
        elif isinstance(other, _Date):
            n = self.to_ordinal() - other.to_ordinal()
            assert 0 < n
            return self.from_ordinal(n)
        raise NotImplementedError

    @classmethod
    def from_date(cls, _date: date | tuple):
        if isinstance(_date, tuple):
            _d = date(*_date[:3])
        elif isinstance(_date, date):
            _d = _date
        else:
            raise TypeError
        solstice = ephem.previous_solstice(str(_d.year)).datetime().date()
        months = _enum_months(_d.year if solstice <= _d else (_d.year - 1))
        last_moon = None
        last_info = None
        for _m in months:
            if months[_m][1] == _d:
                return cls(_d.year, _m[0], 1, _m[1])
            elif months[_m][1] < _d:
                last_moon = _m
                last_info = months[_m]
            else:
                day = (last_info[1] - _d).days
                return cls(_d.year, last_moon[0], day, last_moon[1])

    def to_date(self) -> date:
        months = _enum_months(self._year - (1 if self._month < 11 else 0))
        start = months[(self._month, self._leap)][1]
        return start + timedelta(days=self._day)

    @classmethod
    def from_ordinal(cls, n):
        return cls.from_date(date.fromordinal(n))

    def to_ordinal(self) -> int:
        return self.to_date().toordinal()
