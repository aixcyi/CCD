from datetime import date, timedelta
from typing import NamedTuple, ClassVar, NoReturn

from py_clc.base import ChineseCalendarDate as _Date

DATE_MIN = date(1901, 1, 20)
DATE_MAX = date(2100, 12, 30)
CCD_MIN = (1900, 12, 1, False)
CCD_MAX = (2100, 11, 30, False)
CCD_ORDINAL_MIN = 1  # ChineseCalendarDate.MIN.to_ordinal()
CCD_ORDINAL_MAX = 73029  # ChineseCalendarDate.MAX.to_ordinal()
DATAS = (
    0x1000,  # 1900
    0x0ea4, 0x1d4a, 0xb654, 0x0c96, 0x1536, 0x954d, 0x0ad4, 0x16b2, 0x5754, 0x0ea4,  # 1901-1910
    0xdb4a, 0x164a, 0x1496, 0xb497, 0x055a, 0x0ad6, 0x4b6a, 0x1b52, 0xfd25, 0x1d24,  # 1911-1920
    0x1a4a, 0xba5a, 0x14ac, 0x056c, 0x95ab, 0x0da8, 0x1d52, 0x5e94, 0x1d24, 0xcd4c,  # 1921-1930
    0x0a56, 0x14ae, 0xb2ad, 0x16b4, 0x0da8, 0x6ec3, 0x0e92, 0xf627, 0x1526, 0x0a56,  # 1931-1940
    0xca37, 0x155a, 0x0ad4, 0x9b4b, 0x1748, 0x1692, 0x5a96, 0x152a, 0xf55a, 0x0a6c,  # 1941-1950
    0x155a, 0xb595, 0x0b64, 0x1b4a, 0x7d45, 0x1a94, 0x10b2a, 0x152e, 0x0aac, 0xcaea,  # 1951-1960
    0x15aa, 0x0da4, 0x8eaa, 0x1d4a, 0x0c94, 0x6c9e, 0x1536, 0xf5b4, 0x0ad4, 0x16d2,  # 1961-1970
    0xb764, 0x16a4, 0x164a, 0x9656, 0x1496, 0x11556, 0x055a, 0x0ada, 0xcb53, 0x1b52,  # 1971-1980
    0x1b24, 0x9d2a, 0x1a4a, 0x15c9a, 0x14ac, 0x056c, 0xc5ea, 0x0daa, 0x1d52, 0xbea4,  # 1981-1990
    0x1d24, 0x1a4c, 0x6a5c, 0x14ae, 0x115ac, 0x06b4, 0x0daa, 0xb6d2, 0x0e92, 0x0d26,  # 1991-2000
    0x9536, 0x0a56, 0x14b6, 0x555c, 0x0ad4, 0xfbaa, 0x1748, 0x1692, 0xbaa6, 0x152a,  # 2001-2010
    0x0a5a, 0x8aba, 0x156a, 0x13754, 0x0ba4, 0x1b4a, 0xdd15, 0x1a94, 0x192a, 0x953c,  # 2011-2020
    0x0aac, 0x156a, 0x55b4, 0x0da4, 0xceca, 0x0e4a, 0x0c96, 0xacae, 0x1956, 0x0ab4,  # 2021-2030
    0x6adc, 0x16d2, 0x17ea4, 0x16a4, 0x164a, 0xda17, 0x1496, 0x0956, 0xa576, 0x0b5a,  # 2031-2040
    0x16d4, 0x5b54, 0x1b24, 0xfd4a, 0x1a4a, 0x14aa, 0xb49b, 0x096c, 0x0b6a, 0x6da5,  # 2041-2050
    0x1d92, 0x11f24, 0x1d24, 0x1a4c, 0xca2d, 0x14ae, 0x0aac, 0x86cb, 0x0eaa, 0x0e92,  # 2051-2060
    0x6e96, 0x0d26, 0xf556, 0x0a56, 0x14b6, 0xb574, 0x0ad4, 0x16ca, 0x9754, 0x1694,  # 2061-2070
    0x11b2a, 0x152a, 0x0a5a, 0xcada, 0x156a, 0x0b54, 0x8baa, 0x1b4a, 0x1a94, 0x7c9a,  # 2071-2080
    0x192c, 0xf99c, 0x0aac, 0x156a, 0xb5a5, 0x0da4, 0x1d4a, 0x8e54, 0x0d16, 0x10d2e,  # 2081-2090
    0x0956, 0x0ab6, 0xcaad, 0x16d4, 0x0ea4, 0x972a, 0x168a, 0x1516, 0x549e, 0x0956,  # 2091-2100
)


class Month(NamedTuple):
    year: int
    ordinal: int
    is_leap: bool


class MonthInfo(NamedTuple):
    days: int
    start: date


def _leap_month(yi) -> int:
    """
    从某一年的数据中取出当年的闰月。

    :param yi: 年份索引，从 0 开始表示 1900 年及往后的农历年。
    :return: 月份序数，从 1 开始表示一月及往后的各个平月。为 0 表示当年没有闰月。
    """
    return DATAS[yi] >> 13


def _last_day(yi, mo=0) -> int:
    """
    取出数据中某年某个平月的最后一天。

    :param yi: 年份索引，从 0 开始表示 1900 年及往后的农历年。
    :param mo: 月份序数，从 1 开始表示一月及后面各个平月。如果不提供则表示为当年闰月。
    :return: 当月最后一天的序号，也是当月总天数。
    """
    return (DATAS[yi] >> mo & 1) + 29


def _unzip_months():
    """
    按顺序(解压)生成每个农历月。\n
    每一项都是一个元组，由一个 ``Month`` 和一个 ``MonthInfo`` 组成。
    """
    mos = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)  # 平年所有月份的序数
    start = DATE_MIN.replace()

    # -------- 农历1900年有效数据只有十二月1个平月
    days = _last_day(0, mos[-1])
    yield Month(1900, mos[-1], False), MonthInfo(days, start)
    start += timedelta(days=days)
    # --------
    for yi in range(1, (eyi := len(DATAS) - 1)):  # 1901~2099
        # 平年（没有闰月）
        if (lmo := _leap_month(yi)) == 0:
            for mo in mos:
                days = _last_day(yi, mo)
                yield Month(1900 + yi, mo, False), MonthInfo(days, start)
                start += timedelta(days=days)
        # 闰年（有唯一一个闰月）
        else:
            for mo in mos[:lmo]:
                days = _last_day(yi, mo)
                yield Month(1900 + yi, mo, False), MonthInfo(days, start)
                start += timedelta(days=days)
            # -------- 当年的闰月
            days = _last_day(yi, )
            yield Month(1900 + yi, lmo, True), MonthInfo(days, start)
            start += timedelta(days=days)
            # --------
            for mo in mos[lmo:]:
                days = _last_day(yi, mo)
                yield Month(1900 + yi, mo, False), MonthInfo(days, start)
                start += timedelta(days=days)
    # 农历2100年有效数据只有一到十一月总共11个平月
    for mo in mos[:-1]:
        days = _last_day(eyi, mo)
        yield Month(1900 + eyi, mo, False), MonthInfo(days, start)
        start += timedelta(days=days)


def _calc_ordinals(months: dict[Month, MonthInfo]):
    ordinal = 0
    for m in months:
        yield m, ordinal
        ordinal += months[m].days


# 以月份为键，月份信息为值
MONTHS: dict[Month, MonthInfo] = dict(_unzip_months())

# 以月初公历日期为键，日序数为值
ORDINALS: dict[Month, int] = dict(_calc_ordinals(MONTHS))

# 以月初公历日期为键，月份及总天数为值
NEW_MOONS: dict[date, tuple] = {
    __inf.start: (*__mon, __inf.days)
    for __mon, __inf in MONTHS.items()
}


class ChineseCalendarDate(_Date):
    MIN: ClassVar['ChineseCalendarDate'] = ...
    """
    当前模块支持计算的最早的农历日期。\n
    因为数据没有显示农历1900年十一月是不是闰月，故舍弃。
    """

    MAX: ClassVar['ChineseCalendarDate'] = ...
    """
    当前模块支持计算的最晚的农历日期。\n
    因为数据没有显示农历2100年十二月是大月还是小月，故舍弃。
    """

    # 构造方法 ================================

    def __new__(cls, year, month: int = 1, day: int = 1, is_leap_month: bool = False):
        cls._check_date_fields(year, month, day, is_leap_month)
        self = _Date.__new__(cls, year, month, day, is_leap_month)
        return self

    @classmethod
    def from_date(cls, _date: date):
        """
        将公历日期转换为农历日期。

        :param _date: 公历日期。
        :raise TypeError:
        :raise OverflowError:
        """
        if not isinstance(_date, date):
            raise TypeError(
                '只接受 datetime.date 及其衍生类型的公历日期。'
            )
        if not DATE_MIN <= _date <= DATE_MAX:
            raise OverflowError(
                '公历日期超出农历算法转换范围。'
            )
        starts = list(NEW_MOONS.keys())
        le, ri, mid = 0, len(starts) - 1, len(starts) // 2
        while ri - le > 1:
            if starts[mid] < _date:
                le = mid
            elif starts[mid] > _date:
                ri = mid
            else:
                start = starts[mid]
                break
            mid = le + (ri - le) // 2
        else:
            start = starts[mid]

        y, m, leap, days = NEW_MOONS[start]
        offset = int((_date - start) / timedelta(days=1))
        return _Date.__new__(cls, y, m, offset + 1, leap)

    @classmethod
    def from_ordinal(cls, __n: int):
        if not CCD_ORDINAL_MIN <= __n <= CCD_ORDINAL_MAX:
            raise OverflowError(
                '超出农历日期范围。'
            )
        ordinals = tuple(ORDINALS.values())
        le, ri, mid = 1, len(ordinals) - 1, len(ordinals) // 2
        while ri - le > 1:
            if ordinals[mid] < __n:
                le = mid
            elif ordinals[mid] > __n:
                ri = mid
            else:
                mi = mid
                break
            mid = le + (ri - le) // 2
        else:
            mi = mid

        month = tuple(ORDINALS.keys())[mi]
        y, m, leap = month
        d = __n - ORDINALS[month]
        return _Date.__new__(cls, y, m, d, leap)

    # 只读属性 ================================

    @property
    def days_in_year(self) -> int:
        return sum(inf.days for mt, inf in MONTHS.items() if mt.year == self._year)

    @property
    def days_in_month(self) -> int:
        month = Month(self._year, self._month, self._leap)
        return MONTHS[month].days

    @property
    def day_of_year(self) -> int:
        months = {mt: inf for mt, inf in MONTHS.items() if mt.year == self._year}
        month = Month(self._year, self._month, self._leap)
        return sum(inf.days for mt, inf in months.items() if mt < month) + self._day

    # 计算方法 ================================

    def __add__(self, other):
        if not isinstance(other, timedelta):
            raise TypeError(
                'can only add datetime.timedelta '
                '(not {0}.{1}) into {2}{3}'.format(
                    other.__class__.__module__,
                    other.__class__.__qualname__,
                    self.__class__.__module__,
                    self.__class__.__qualname__,
                )
            )
        if (delta := other.days) == 0:
            return self._replace()
        if delta < 0:
            return self.__sub__(-other)
        return self.from_ordinal(self.to_ordinal() + delta)

    __radd__ = __add__

    def __sub__(self, other):
        if not isinstance(other, timedelta):
            raise TypeError(
                'can only subtract datetime.timedelta '
                '(not {0}.{1}) with {2}{3}'.format(
                    other.__class__.__module__,
                    other.__class__.__qualname__,
                    self.__class__.__module__,
                    self.__class__.__qualname__,
                )
            )
        if (delta := other.days) == 0:
            return self.replace()
        if delta < 0:
            return self.__add__(-other)
        return self.from_ordinal(self.to_ordinal() - delta)

    # 转换器 ================================

    def to_date(self) -> date:
        """
        将当前的农历日期转换为公历日期。
        """
        month = Month(self._year, self._month, self._leap)
        return MONTHS[month].start + timedelta(days=self._day - 1)

    def to_ordinal(self) -> int:
        month = Month(self._year, self._month, self._leap)
        return ORDINALS[month] + self._day

    # 其它方法 ================================

    @classmethod
    def _check_date_fields(cls,
                           year: int,
                           month: int,
                           day: int,
                           is_leap_month: bool) -> NoReturn:
        # 类型检查
        y, m, d, leap = year, month, day, is_leap_month
        super()._check_date_fields(y, m, d, leap)

        # 精度检查
        if not CCD_MIN <= (y, m, d, leap) <= CCD_MAX:
            raise OverflowError(
                '超出精度范围。请使用更高精度的历法算法。\n'
                '本类支持的精度范围是：{0} 至 {1}'.format(
                    ChineseCalendarDate.MIN.strftime(),
                    ChineseCalendarDate.MAX.strftime(),
                )
            )
        prefix = '闰' if leap else ''
        if (month := Month(y, m, leap)) not in MONTHS:
            raise ValueError(
                f'农历{y}年没有{prefix}{m}月。'
            )
        if not d <= MONTHS[month].days:
            raise ValueError(
                f'提供的农历日 {d} 不在农历{y}年{prefix}{m}月中。'
            )


ChineseCalendarDate.MIN = ChineseCalendarDate(*CCD_MIN)
ChineseCalendarDate.MAX = ChineseCalendarDate(*CCD_MAX)
