"""
定义农历日期的抽象类，其中实现了农历日期文本与数字转换的功能。
"""

from datetime import date
from typing import NoReturn

STEMS = '甲乙丙丁戊己庚辛壬癸'
BRANCHES = '子丑壬卯辰巳午未申酉戌亥'
ZODIACS = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
MONTHS = {
    1: '正', 2: '二', 3: '三', 4: '四', 5: '五', 6: '六',
    7: '七', 8: '八', 9: '九', 10: '十', 11: '十一', 12: '十二',
}
DAYS = {
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


class ChineseCalendarDate(object):
    __slots__ = '_year', '_month', '_day', '_leap', '_hashcode'

    def __new__(cls, year, month: int = 1, day: int = 1, is_leap_month: bool = False):
        """
        农历日期。

        Concrete date of Chinese lunisolar calendar.

        :param year: 农历年份。
        :param month: 农历月份。
        :param day: 农历日。
        :param is_leap_month: 农历月是否为闰月。
        :raise TypeError: 日期参数类型有误。
        :raise ValueError: 日期参数值有误。
        :raise OverflowError: 日期超出精度范围。
        """
        self = object.__new__(cls)
        self._year = year
        self._month = month
        self._day = day
        self._leap = is_leap_month
        self._hashcode = -1
        return self

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

    def _replace(self, year=None, month=None, day=None, is_leap_month=None):
        return ChineseCalendarDate.__new__(
            type(self),
            self._year if year is None else year,
            self._month if month is None else month,
            self._day if day is None else day,
            self._leap if is_leap_month not in (True, False) else is_leap_month,
        )

    # 静态方法 ================================

    @classmethod
    def _check_date_fields(cls,
                           year: int,
                           month: int,
                           day: int,
                           is_leap_month: bool) -> NoReturn:
        """
        检查组成农历日期的字段是否正确。

        :param year: 农历年份。
        :param month: 农历月份。
        :param day: 农历日。
        :param is_leap_month: 提供的农历月份是否为闰月。
        :return: 无返回值。
        :raise TypeError:
        :raise ValueError:
        :raise OverflowError:
        """
        if (
                not isinstance(year, int) or
                not isinstance(month, int) or
                not isinstance(day, int)
        ):
            raise TypeError('year、month、day 必须是整数类型。')
        if is_leap_month not in (True, False):
            raise TypeError('is_leap_month 必须是布尔类型。')
        if not 1 <= month <= 12:
            raise ValueError('农历月只能是一个从 1 到 12 的整数。')
        if not 1 <= day <= 30:
            raise ValueError('农历日只能是一个从 1 到 30 的整数。')

    # 只读属性 ================================

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
        raise NotImplementedError

    @property
    def days_in_month(self) -> int:
        """当月总共有多少天。"""
        raise NotImplementedError

    @property
    def day_of_year(self) -> int:
        """当天是自正月初一开始的第几天。"""
        raise NotImplementedError

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

        不会以 ”月“ 结尾。

        除了第一个月使用 ”正月“ 表达外，其它月份都与小写数字无异。
        比如 ”六月“、”十二月“ 等。
        """
        return MONTHS[self._month]

    @property
    def day_ordinal(self) -> str:
        """
        序数纪日法表示的农历日。

        比如 ”初一“、”十五“、”廿九“ 等。
        """
        return DAYS[self._day]

    # 比较器 ================================

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

    # 历法推算 ================================

    def __add__(self, other):
        raise NotImplementedError

    def __radd__(self, other):
        raise NotImplementedError

    def __sub__(self, other):
        raise NotImplementedError

    # 基本转换 ================================

    def __hash__(self):
        if self._hashcode == -1:
            yhi, ylo = divmod(self._year, 256)
            mon = self._month | (128 if self._leap else 0)
            code = bytes([yhi, ylo, mon, self._day])
            self._hashcode = hash(code)
        return self._hashcode

    def timetuple(self) -> tuple:
        """获取组成日期的所有部分。"""
        return self._year, self._month, self._day, self._leap

    # 与字符串相关的转换 ================================

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

    @classmethod
    def strptime(cls, string, fmt: str):
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
        # TODO
        pass

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

        def translate():
            leap = '闰' if self._leap else ''
            i, n = 0, len(fmt)
            while i < n:
                if fmt[i] != '%':
                    yield fmt[i]
                elif i == n - 1:  # 枚举到最后一个字符
                    raise ValueError(f'无法解析格式化符号 "%"，所在位置 {i}')
                else:
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
                            yield leap + MONTHS[self._month]
                        case 'a':
                            yield DAYS[self._day]
                        case '%':
                            yield '%'
                            continue
                        case _:
                            raise ValueError(f'无法解析格式化符号 "%{flag}"，所在位置 {i}')
                i += 1

        return ''.join(translate())

    # 与 datetime.date 相关的转换 ================================

    @classmethod
    def today(cls):
        """获取今天对应的农历日期。"""
        return cls.from_date(date.today())

    @classmethod
    def from_date(cls, _date: date):
        """将公历日期转换为农历日期。"""
        raise NotImplementedError

    def to_date(self) -> date:
        """将当前的农历日期转换为公历日期。"""
        raise NotImplementedError

    fromdate = from_date
    todate = to_date

    # 与 ordinal 相关的转换 ================================

    @classmethod
    def from_ordinal(cls, __n: int):
        raise NotImplementedError(
            '{0}.{1} 并不会实现此方法，请勿使用。'.format(
                cls.__module__,
                cls.__qualname__,
            )
        )

    def to_ordinal(self) -> int:
        raise NotImplementedError(
            '{0}.{1} 并不会实现此方法，请勿使用。'.format(
                self.__class__.__module__,
                self.__class__.__qualname__,
            )
        )

    fromordinal = from_ordinal
    toordinal = to_ordinal
