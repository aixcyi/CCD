"""
定义农历日期的抽象类，其中实现了农历日期文本与数字转换的功能。
"""
import re
from datetime import date, timedelta
from typing import NamedTuple, NoReturn

STEMS = '甲乙丙丁戊己庚辛壬癸'
BRANCHES = '子丑寅卯辰巳午未申酉戌亥'
ZODIACS = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
ORDS_MON = {
    1: '正', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六',
    7: '七', 8: '八', 9: '九', 10: '十', 11: '十一', 12: '十二',
}
ORDS_DAY = {
    1: '初一', 11: '十一', 21: '廿一',
    2: '初二', 12: '十二', 22: '廿二',
    3: '初三', 13: '十三', 23: '廿三',
    4: '初四', 14: '十四', 24: '廿四',
    5: '初五', 15: '十五', 25: '廿五',
    6: '初六', 16: '十六', 26: '廿六',
    7: '初七', 17: '十七', 27: '廿七',
    8: '初八', 18: '十八', 28: '廿八',
    9: '初九', 19: '十九', 29: '廿九',
    10: '初十', 20: '二十', 30: '三十',
}
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
CHARS_MON = {v: k for k, v in ORDS_MON.items()} | {'冬': 11, '腊': 12}
CHARS_DAY = {v: k for k, v in ORDS_DAY.items()} | {'卄': 20, '卅': 30}


def _check_date_fields(y, m, d, leap) -> NoReturn:
    """
    检查农历日期字段的类型和普遍适用的范围。

    :return: 无返回值。
    :raise TypeError: 参数类型错误。
    :raise ValueError: 参数错误或无法转换。
    """
    if (
            not isinstance(y, int) or
            not isinstance(m, int) or
            not isinstance(d, int)
    ):
        raise TypeError('year、month、day 必须是整数类型。')
    if leap is not True and leap is not False:
        raise TypeError('is_leap_month 必须是布尔类型。')
    if not 1 <= m <= 12:
        raise ValueError('农历月只能是一个从 1 到 12 的整数。')
    if not 1 <= d <= 30:
        raise ValueError('农历日只能是一个从 1 到 30 的整数。')


def _check_date_range(y, m, d, leap) -> NoReturn:
    """
    检查农历日期字段的范围。

    :return: 无返回值。
    :raise ValueError: 参数错误或无法转换。
    :raise OverflowError: 参数超出可计算范围。
    """
    if not CCD_MIN <= (y, m, d, leap) <= CCD_MAX:
        raise OverflowError(
            '超出支持范围。请使用范围更广的历法算法。\n'
            '本类支持的范围是：{0} 至 {1}'.format(
                ChineseCalendarDate.MIN.strftime(),
                ChineseCalendarDate.MAX.strftime(),
            )
        )
    prefix = '闰' if leap else ''
    if (month := Month(y, m, leap)) not in MONTHS:
        raise ValueError(
            f'农历 {y}年 没有 {prefix}{m}月。'
        )
    if not d <= MONTHS[month].days:
        raise ValueError(
            f'农历 {y}年 {prefix}{m}月 没有 {d} 日。'
        )


def _compile(fmt):
    if fmt.__class__ is not str:
        raise TypeError(
            '请以字符串形式提供农历日期格式。'
        )
    i, length = 0, len(fmt)
    while i < length:
        if (c := fmt[i]) != '%':
            yield c
        else:
            if i + 1 == length:
                raise ValueError(
                    f'无法解析格式化符号 "%"，所在位置 {i}'
                )
            match (c := fmt[(i := i + 1)]):
                case 'Y':
                    yield r'(?P<year>[0-9]{1,})'
                case 'm':
                    yield r'(?P<month>[闰閏]?(0[1-9]|1[012]))'
                case 'd':
                    yield r'(?P<day>[1-9]|[12][0-9]|30)'
                case 'b':
                    yield r'(?P<month>[闰閏]?([正二三四五六七八九冬腊]|十一|十二))'
                case 'a':
                    yield r'(?P<day>[初十廿][一二三四五六七八九]|[初二三]十|[卄卅])'
                case '%':
                    yield r'%'
                case _:
                    raise ValueError(
                        f'无法解析格式化符号 "{c}"，所在位置 {i}'
                    )
        i += 1


def _strftime(self, fmt):
    leap = '闰' if self._leap else ''
    i, n = 0, len(fmt)
    while i < n:
        if fmt[i] != '%':
            yield fmt[i]
        else:
            if i == n - 1:  # 枚举到最后一个字符
                raise ValueError(f'无法解析格式化符号 "%"，所在位置 {i}')
            match (flag := fmt[i := i + 1]):  # 取下一个字符
                case 'Y':
                    yield f'{self._year:04d}'
                case 'm':
                    yield f'{self._month:02d}'
                case 'd':
                    yield f'{self._day:02d}'
                case 'G':
                    yield self.year_stem_branch
                case 'g':
                    yield self.year_zodiac
                case 'b':
                    yield leap + ORDS_MON[self._month]
                case 'a':
                    yield ORDS_DAY[self._day]
                case '%':
                    yield '%'
                case _:
                    raise ValueError(f'无法解析格式化符号 "%{flag}"，所在位置 {i}')
        i += 1


class Month(NamedTuple):
    year: int
    ordinal: int
    is_leap: bool


class MonthInfo(NamedTuple):
    days: int
    start: date
    ordinal: int


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
    ordinal = CCD_ORDINAL_MIN

    # -------- 农历1900年有效数据只有十二月1个平月
    days = _last_day(0, mos[-1])
    yield Month(1900, mos[-1], False), MonthInfo(days, start, ordinal)
    start += timedelta(days=days)
    ordinal += days
    # --------
    for yi in range(1, (eyi := len(DATAS) - 1)):  # 1901~2099
        # 平年（没有闰月）
        if (lmo := _leap_month(yi)) == 0:
            for mo in mos:
                days = _last_day(yi, mo)
                yield Month(1900 + yi, mo, False), MonthInfo(days, start, ordinal)
                start += timedelta(days=days)
                ordinal += days
        # 闰年（有唯一一个闰月）
        else:
            for mo in mos[:lmo]:
                days = _last_day(yi, mo)
                yield Month(1900 + yi, mo, False), MonthInfo(days, start, ordinal)
                start += timedelta(days=days)
                ordinal += days
            # -------- 当年的闰月
            days = _last_day(yi, )
            yield Month(1900 + yi, lmo, True), MonthInfo(days, start, ordinal)
            start += timedelta(days=days)
            ordinal += days
            # --------
            for mo in mos[lmo:]:
                days = _last_day(yi, mo)
                yield Month(1900 + yi, mo, False), MonthInfo(days, start, ordinal)
                start += timedelta(days=days)
                ordinal += days
    # 农历2100年有效数据只有一到十一月总共11个平月
    for mo in mos[:-1]:
        days = _last_day(eyi, mo)
        yield Month(1900 + eyi, mo, False), MonthInfo(days, start, ordinal)
        start += timedelta(days=days)
        ordinal += days


# 以月份为键，月份信息为值
MONTHS: dict[Month, MonthInfo] = dict(_unzip_months())

# 以月初公历日期为键，月份及总天数为值
NEW_MOONS: dict[date, tuple] = {
    __inf.start: (*__mon, __inf.days)
    for __mon, __inf in MONTHS.items()
}


class ChineseCalendarDate(object):
    __slots__ = '_year', '_month', '_day', '_leap', '_hashcode'

    # 构造方法

    def __new__(cls, year, month=1, day=1, is_leap_month: bool = False):
        """
        农历日期。

        Concrete date of Chinese lunisolar calendar.

        :param year: 农历年份。
        :param month: 农历月份。
        :param day: 农历日。
        :param is_leap_month: 农历月是否为闰月。
        :raise TypeError: 参数类型有误。
        :raise ValueError: 参数有误或无法转换。
        :raise OverflowError: 参数超出计算范围。
        """
        _check_date_fields(year, month, day, is_leap_month)
        _check_date_range(year, month, day, is_leap_month)
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._leap = is_leap_month
        self._hashcode = -1
        return self

    @classmethod
    def strptime(cls, string, fmt: str = '农历%Y年%b月%a'):
        """
        将一个字符串按照指定格式转换为农历日期。

        可用的格式化符号有：

        - ``%Y`` ，补零后，用十进制数字表示的农历年，比如“1901”。
        - ``%m`` ，补零后，用十进制数字表示的农历月，比如”01“、”06“、”12“。
        - ``%d`` ，补零后，用十进制数字表示的农历日，比如”01“、”15“、”21“。
        - ``%b`` ，数序纪月法表示的农历月，比如“正”、“十一”、“十二”，闰月比如“闰七”。
        - ``%a`` ，序数纪日法表示的农历日，比如“初一”、“十五”、“廿一”。
        - ``%%`` ，符号 "%" 自身。

        :param string: 字符串。
        :param fmt: 格式。必须与字符串完全匹配。
        :return: 农历日期。
        """
        regex = ''.join(_compile(fmt))
        result = re.fullmatch(regex, string)
        if result is None:
            raise ValueError(
                f'日期字符串 "{string} 与指定格式 "{fmt}" 不匹配。'
            )
        data = result.groupdict()
        y, m, d = data.get('year'), data.get('month'), data.get('day')
        if y is None or m is None or d is None:
            raise ValueError(
                f'日期缺少年、月或日。'
            )
        y = int(y)
        leap = m.startswith('闰') or m.startswith('閏')
        m = m[1:] if leap else m
        try:
            m = int(m) if m.isdecimal() else CHARS_MON[m]
            d = int(d) if d.isdecimal() else CHARS_DAY[d]
        except KeyError as e:
            raise ValueError(
                f'无法识别的表述："{e.args[0]}"'
            ) from None
        return cls(y, m, d, leap)

    @classmethod
    def today(cls) -> 'ChineseCalendarDate':
        """获取今天对应的农历日期。"""
        return cls.from_date(date.today())

    @classmethod
    def from_date(cls, _date: date) -> 'ChineseCalendarDate':
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
        return cls.__new__(cls, y, m, offset + 1, leap)

    @classmethod
    def from_ordinal(cls, __n: int) -> 'ChineseCalendarDate':
        if not CCD_ORDINAL_MIN <= __n <= CCD_ORDINAL_MAX:
            raise OverflowError(
                '超出农历日期范围。'
            )
        ordinals = tuple(v.ordinal for v in MONTHS.values())
        le, ri, mid = 0, len(ordinals) - 1, len(ordinals) // 2
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

        month = tuple(MONTHS.keys())[mi]
        y, m, leap = month
        d = __n - MONTHS[month].ordinal
        return cls.__new__(cls, y, m, d, leap)

    fromordinal = from_ordinal

    def _replace(self, year=None, month=None, day=None, is_leap_month=None):
        return ChineseCalendarDate.__new__(
            type(self),
            self._year if year is None else year,
            self._month if month is None else month,
            self._day if day is None else day,
            self._leap if is_leap_month not in (True, False) else is_leap_month,
        )

    def replace(self, year=None, month=None, day=None, is_leap_month=None):
        """
        使用日期的一部分替换当前的日期，从而生成一个新的农历日期。

        :param year: 新的农历年。如不提供则使用当前的农历年。
        :param month: 新的农历月。如不提供则使用当前的农历月。
        :param day: 新的农历日。如不提供则使用当前的农历日。
        :param is_leap_month: 是否为闰月。如不指定则默认为当前日期的设置。
        :return: 一个新的农历日期。无论是否提供任何参数。
        """
        return type(self)(
            self._year if year is None else year,
            self._month if month is None else month,
            self._day if day is None else day,
            self._leap if is_leap_month not in (True, False) else is_leap_month,
        )

    # 只读属性

    @property
    def year(self) -> int:
        """农历年份。"""
        return self._year

    @property
    def month(self) -> int:
        """农历月份。取值范围是 ``1`` 到 ``12`` 。"""
        return self._month

    @property
    def day(self) -> int:
        """农历日（即，这个月的第几天）。取值范围是 ``1`` 到 ``30`` 。"""
        return self._day

    @property
    def is_leap_month(self) -> bool:
        """当月是否为闰月。"""
        return self._leap

    @property
    def days_in_year(self) -> int:
        """当年总共有多少天。"""
        return sum(inf.days for mt, inf in MONTHS.items() if mt.year == self._year)

    @property
    def days_in_month(self) -> int:
        """当月总共有多少天。"""
        month = Month(self._year, self._month, self._leap)
        return MONTHS[month].days

    @property
    def day_of_year(self) -> int:
        """当天是自正月初一开始的第几天。"""
        months = {mt: inf for mt, inf in MONTHS.items() if mt.year == self._year}
        month = Month(self._year, self._month, self._leap)
        return sum(inf.days for mt, inf in months.items() if mt < month) + self._day

    @property
    def year_stem_branch(self) -> str:
        """
        干支纪年法表示的农历年。

        比如农历 1894 年对应的是 "甲午" 。
        """
        # 农历4年是正数年份的第一个甲子年。
        # ISO 8601 约定了负数年份：0 表示公元前 1 年，1表示公元前 2 年，以此类推；
        # 负数可以被正确求余，所以这里不需要处理。
        year = self._year - 4
        return STEMS[year % 10] + BRANCHES[year % 12]

    @property
    def year_zodiac(self) -> str:
        """
        生肖纪年法表示的农历年。

        比如农历 1894 年对应的是 "马" 。
        """
        return ZODIACS[(self._year - 4) % 12]

    @property
    def month_ordinal(self) -> str:
        """
        数序纪月法表示的农历月份。

        第一个月使用 “正”月 表述，
        往后的月份均使用小写数字表示，比如 “六”月、“十二”月。

        不会以 ”月“ 结尾。当该月是闰月时会以 “闰” 开头。
        """
        prefix = '闰' if self._leap else ''
        return prefix + ORDS_MON[self._month]

    @property
    def day_ordinal(self) -> str:
        """
        序数纪日法表示的农历日。

        比如 ”初一“、”十五“、”廿九“ 等。
        """
        return ORDS_DAY[self._day]

    # 比较器

    def __eq__(self, other):
        if isinstance(other, ChineseCalendarDate):
            return self._cmp(other) == 0
        raise NotImplementedError

    def __le__(self, other):
        if isinstance(other, ChineseCalendarDate):
            return self._cmp(other) <= 0
        raise NotImplementedError

    def __lt__(self, other):
        if isinstance(other, ChineseCalendarDate):
            return self._cmp(other) < 0
        raise NotImplementedError

    def __ge__(self, other):
        if isinstance(other, ChineseCalendarDate):
            return self._cmp(other) >= 0
        raise NotImplementedError

    def __gt__(self, other):
        if isinstance(other, ChineseCalendarDate):
            return self._cmp(other) > 0
        raise NotImplementedError

    def _cmp(self, other):
        assert isinstance(other, ChineseCalendarDate)
        x = self.timetuple()
        y = other.timetuple()
        return 0 if x == y else 1 if x > y else -1

    # 计算方法

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

    # 转换器

    def __hash__(self):
        if self._hashcode == -1:
            yhi, ylo = divmod(self._year, 256)
            mon = self._month | (128 if self._leap else 0)
            code = bytes([yhi, ylo, mon, self._day])
            self._hashcode = hash(code)
        return self._hashcode

    def __repr__(self):
        return '%s.%s(%d, %d, %d, %s)' % (
            self.__class__.__module__,
            self.__class__.__qualname__,
            self._year,
            self._month,
            self._day,
            self._leap,
        )

    def __str__(self):
        return self.strftime()

    def timetuple(self) -> tuple:
        """获取组成日期的所有部分。"""
        return self._year, self._month, self._day, self._leap

    def strftime(self, fmt: str = '农历%Y年%b月%a') -> str:
        """
        将农历日期按照指定格式转换为一个字符串。

        可用的格式化符号有：

        - ``%Y`` ，补零后，用十进制数字表示的农历年，比如“1901”。
        - ``%m`` ，补零后，用十进制数字表示的农历月，比如”01“、”06“、”12“。
        - ``%d`` ，补零后，用十进制数字表示的农历日，比如”01“、”15“、”21“。
        - ``%G`` ，干支纪年法表示的农历年，比如“庚寅”。
        - ``%g`` ，生肖纪年法表示的农历年，比如“虎”。
        - ``%b`` ，数序纪月法表示的农历月，比如“正”、“十一”、“十二”，闰月比如“闰七”。
        - ``%a`` ，序数纪日法表示的农历日，比如“初一”、“十五”、“廿一”。
        - ``%%`` ，符号 "%" 自身。

        默认省略年月中的后缀“年”和“月”。如有需要，请在格式中手动添加，比如

            "%G%g年%b月%d" 可以格式化为 “庚寅虎年正月廿二”

        :param fmt: 格式。
        :return: 格式化后产生的字符串。
        :raise ValueError: 格式无法解析时抛出。
        """
        return ''.join(_strftime(self, fmt))

    def to_date(self) -> date:
        """将当前的农历日期转换为公历日期。"""
        month = Month(self._year, self._month, self._leap)
        return MONTHS[month].start + timedelta(days=self._day - 1)

    def to_ordinal(self) -> int:
        month = Month(self._year, self._month, self._leap)
        return MONTHS[month].ordinal + self._day

    toordinal = to_ordinal


ChineseCalendarDate.MIN = ChineseCalendarDate(*CCD_MIN)
"""
当前模块支持计算的最早的农历日期。\n
因为数据没有显示农历1900年十一月是不是闰月，故舍弃。
"""

ChineseCalendarDate.MAX = ChineseCalendarDate(*CCD_MAX)
"""
当前模块支持计算的最晚的农历日期。\n
因为数据没有显示农历2100年十二月是大月还是小月，故舍弃。
"""

if __name__ == '__main__':
    gcd = date(2020, 6, 20)
    ccd = ChineseCalendarDate.from_date(gcd)
    assert ccd.timetuple() == (2020, 4, 29, True)
    assert str(ccd) == '农历2020年闰四月廿九'
    assert ccd.day_of_year == 148  # 这一天是当年的第148天
    assert ccd.days_in_year == 384  # 农历2020年总共384天（2020.1.25-2021.2.11）
    assert ccd.days_in_month == 29  # 农历2020年闰四月总共29天
    assert ccd.year_stem_branch == '庚子'
    assert ccd.year_zodiac == '鼠'
    assert ccd.month_ordinal == '闰四'
    assert ccd.day_ordinal == '廿九'
    assert ccd == ChineseCalendarDate(2020, 4, 29, True)
    assert ccd < ChineseCalendarDate(2020, 5, 1, False)
    assert ccd > ChineseCalendarDate(2020, 4, 28, True)

    ccd = ChineseCalendarDate.fromordinal(CCD_ORDINAL_MIN)
    assert ccd.timetuple() == CCD_MIN
    ccd = ChineseCalendarDate.fromordinal(CCD_ORDINAL_MAX)
    assert ccd.timetuple() == CCD_MAX

    ccd2 = ccd + timedelta(days=0)
    assert ccd.timetuple() == ccd2.timetuple()
    assert id(ccd) != id(ccd2)
    ccd2 = ccd - timedelta(days=0)
    assert ccd.timetuple() == ccd2.timetuple()
    assert id(ccd) != id(ccd2)

    ccd += timedelta(days=1)
    assert ccd.timetuple() == (2020, 5, 1, False)
    ccd -= timedelta(days=1)
    assert ccd.timetuple() == (2020, 4, 29, True)
    ccd -= timedelta(days=-1)
    assert ccd.timetuple() == (2020, 5, 1, False)
    ccd += timedelta(days=-1)
    assert ccd.timetuple() == (2020, 4, 29, True)

    ccd = ChineseCalendarDate.strptime('农历2020年闰四月廿九', '农历%Y年%b月%a')
    assert ccd.timetuple() == (2020, 4, 29, True)
