from collections import OrderedDict
from datetime import date
from typing import ClassVar

from lunisolar.chinese.base import (
    ChineseCalendarDate as _Date,
    _check_date_fields_basic,
)

DATE_MIN = (1901, 1, 20)
DATE_MAX = (2100, 12, 30)
ORDINAL_OFFSET = date(*DATE_MIN).toordinal() - 1

CCD_MIN = (1900, 12, 1, False)
CCD_MAX = (2100, 11, 30, False)
CCD_ORDINAL_MIN = 1  # ChineseCalendarDate.min.to_ordinal()
CCD_ORDINAL_MAX = 73029  # ChineseCalendarDate.max.to_ordinal()
INFO_LIST = [
    0x0800,  # 1900
    0x0752, 0x0ea5, 0xab2a, 0x064b, 0x0a9b, 0x9aa6, 0x056a, 0x0b59, 0x4baa, 0x0752,  # 1901-1910
    0xcda5, 0x0b25, 0x0a4b, 0xba4b, 0x02ad, 0x056b, 0x45b5, 0x0da9, 0xfe92, 0x0e92,  # 1911-1920
    0x0d25, 0xad2d, 0x0a56, 0x02b6, 0x9ad5, 0x06d4, 0x0ea9, 0x4f4a, 0x0e92, 0xc6a6,  # 1921-1930
    0x052b, 0x0a57, 0xb956, 0x0b5a, 0x06d4, 0x7761, 0x0749, 0xfb13, 0x0a93, 0x052b,  # 1931-1940
    0xd51b, 0x0aad, 0x056a, 0x9da5, 0x0ba4, 0x0b49, 0x4d4b, 0x0a95, 0xeaad, 0x0536,  # 1941-1950
    0x0aad, 0xbaca, 0x05b2, 0x0da5, 0x7ea2, 0x0d4a, 0x10595, 0x0a97, 0x0556, 0xc575,  # 1951-1960
    0x0ad5, 0x06d2, 0x8755, 0x0ea5, 0x064a, 0x664f, 0x0a9b, 0xeada, 0x056a, 0x0b69,  # 1961-1970
    0xabb2, 0x0b52, 0x0b25, 0x8b2b, 0x0a4b, 0x10aab, 0x02ad, 0x056d, 0xd5a9, 0x0da9,  # 1971-1980
    0x0d92, 0x8e95, 0x0d25, 0x14e4d, 0x0a56, 0x02b6, 0xc2f5, 0x06d5, 0x0ea9, 0xaf52,  # 1981-1990
    0x0e92, 0x0d26, 0x652e, 0x0a57, 0x10ad6, 0x035a, 0x06d5, 0xab69, 0x0749, 0x0693,  # 1991-2000
    0x8a9b, 0x052b, 0x0a5b, 0x4aae, 0x056a, 0xedd5, 0x0ba4, 0x0b49, 0xad53, 0x0a95,  # 2001-2010
    0x052d, 0x855d, 0x0ab5, 0x12baa, 0x05d2, 0x0da5, 0xde8a, 0x0d4a, 0x0c95, 0x8a9e,  # 2011-2020
    0x0556, 0x0ab5, 0x4ada, 0x06d2, 0xc765, 0x0725, 0x064b, 0xa657, 0x0cab, 0x055a,  # 2021-2030
    0x656e, 0x0b69, 0x16f52, 0x0b52, 0x0b25, 0xdd0b, 0x0a4b, 0x04ab, 0xa2bb, 0x05ad,  # 2031-2040
    0x0b6a, 0x4daa, 0x0d92, 0xeea5, 0x0d25, 0x0a55, 0xba4d, 0x04b6, 0x05b5, 0x76d2,  # 2041-2050
    0x0ec9, 0x10f92, 0x0e92, 0x0d26, 0xd516, 0x0a57, 0x0556, 0x9365, 0x0755, 0x0749,  # 2051-2060
    0x674b, 0x0693, 0xeaab, 0x052b, 0x0a5b, 0xaaba, 0x056a, 0x0b65, 0x8baa, 0x0b4a,  # 2061-2070
    0x10d95, 0x0a95, 0x052d, 0xc56d, 0x0ab5, 0x05aa, 0x85d5, 0x0da5, 0x0d4a, 0x6e4d,  # 2071-2080
    0x0c96, 0xecce, 0x0556, 0x0ab5, 0xbad2, 0x06d2, 0x0ea5, 0x872a, 0x068b, 0x10697,  # 2081-2090
    0x04ab, 0x055b, 0xd556, 0x0b6a, 0x0752, 0x8b95, 0x0b45, 0x0a8b, 0x4a4f, 0x04ab,  # 2091-2100
]


def _unzip_year(i):
    def _last_day(_month):
        return 30 if INFO_LIST[i] >> _month & 1 > 0 else 29

    year = 1900 + i
    if year == 1900:
        return {(12, False): _last_day(11)}
    if year == 2100:
        return {(_m + 1, False): _last_day(_m) for _m in range(11)}

    if not (_leap := INFO_LIST[i] >> 13):
        return {(m + 1, False): _last_day(m) for m in range(12)}
    months = [((m + 1, False), _last_day(m)) for m in range(12)] + [((_leap, True), _last_day(12))]
    months.sort()
    return dict(months)


CCD_INFO: dict[int, dict[tuple[int, bool], int]] = {
    1900 + i: _unzip_year(i) for i in range(len(INFO_LIST))
}


def _check_date_fields(year: int, month: int, day: int, is_leap_month: bool):
    _check_date_fields_basic(year, month, day, is_leap_month)
    if not CCD_MIN <= (year, month, day, is_leap_month) <= CCD_MAX:
        raise OverflowError('超出精度范围。请使用更高精度的 Calendar。')

    if (_month := (month, is_leap_month)) not in CCD_INFO[year]:
        tip = '闰' if is_leap_month else ''
        raise ValueError(f'农历{year}年没有{tip}{month}月。')
    if not day <= CCD_INFO[year][_month]:
        raise ValueError(f'提供的农历日 {day} 超过了当月日期范围。')


class ChineseCalendarDate(_Date):
    min: ClassVar['ChineseCalendarDate'] = ...
    """
    当前模块支持计算的最早的农历日期。\n
    因为数据没有显示农历1900年十一月是不是闰月，故截断。
    """

    max: ClassVar['ChineseCalendarDate'] = ...
    """
    当前模块支持计算的最晚的农历日期。\n
    因为数据没有显示农历2100年十二月是大月还是小月，故截断。
    """

    def __new__(cls, year: int, month=1, day=1, is_leap_month: bool = False):
        _check_date_fields(year, month, day, is_leap_month)
        self = _Date.__new__(cls, year, month, day, is_leap_month)
        return self

    # 历法推算 ================================

    @staticmethod
    def months(_year: int) -> OrderedDict[tuple[int, bool], int | tuple]:
        maps = OrderedDict(CCD_INFO[_year])
        for month, days in maps.items():
            start = ChineseCalendarDate(_year, month[0], 1, month[1]).to_date()
            maps[month] = (days, start)
        return maps

    def get_days_in_year(self) -> int:
        return sum(CCD_INFO[self._year].values())

    def get_days_in_month(self) -> int:
        return CCD_INFO[self._year][(self._month, self._is_leap_month)]

    def get_day_of_year(self) -> int:
        months = CCD_INFO[self._year]
        _month = (self._month, self._is_leap_month)
        return sum(days for m, days in months.items() if m < _month) + self._day

    # 与 datetime.date 相关的转换 ================================

    @classmethod
    def from_date(cls, _date: date | tuple):
        """将公历日期转换为农历日期。"""
        if isinstance(_date, tuple):
            _d = date(*_date[:3])
        elif isinstance(_date, date):
            _d = date
        else:
            raise TypeError
        assert 0 < (n := _d.toordinal() - ORDINAL_OFFSET)
        return cls.from_ordinal(n)

    def to_date(self) -> date:
        """将当前的农历日期转换为公历日期。"""
        return date.fromordinal(ORDINAL_OFFSET + self.to_ordinal())

    # 与日戳相关的转换 ================================

    @classmethod
    def from_ordinal(cls, n: int):
        assert CCD_ORDINAL_MIN <= n <= CCD_ORDINAL_MAX
        if n <= (d := CCD_INFO[1900][(12, False)]):
            _y, _m, _d, _leap = CCD_MIN
            _d = n
            return cls(_y, _m, _d, _leap)
        n -= d

        # 按年循环减扣日戳 ----------------
        year = 1901
        while n > (days := sum(CCD_INFO[year].values())):
            n -= days
            year += 1

        # 按月循环减扣日戳 ----------------
        months = CCD_INFO[year]
        for month, days in months.items():
            if n > days:
                n -= days
            else:
                return cls(year, month[0], n, month[1])

    def to_ordinal(self) -> int:
        return self.get_day_of_year() + sum(
            sum(CCD_INFO[y].values()) for y in range(CCD_MIN[0], self._year)
        )


ChineseCalendarDate.min = ChineseCalendarDate(*CCD_MIN)
ChineseCalendarDate.max = ChineseCalendarDate(*CCD_MAX)


def __check_translation():
    for i in range(73000, CCD_ORDINAL_MAX + 1):
        print(f'{i}\t', ChineseCalendarDate.from_ordinal(i))
    print(ChineseCalendarDate.max.to_ordinal())
    print(ChineseCalendarDate(*CCD_MAX).to_ordinal())


def __speed_test():
    from datetime import date, datetime
    # from lunisolar.chinese.limited import ChineseCalendarDate

    stamp = datetime.now().timestamp()
    for i in range(1, date.max.toordinal() + 1):
        str(date.fromordinal(i))
    stamp = datetime.now().timestamp() - stamp
    print(stamp)

    stamp = datetime.now().timestamp()
    for i in range(1, 73030):
        str(ChineseCalendarDate.from_ordinal(i))
    stamp = datetime.now().timestamp() - stamp
    print(stamp)


if __name__ == '__main__':
    __speed_test()
