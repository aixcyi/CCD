from datetime import date
from typing import ClassVar

from lunisolar.chinese.base import ChineseCalendarDate as _Date

DATE_MIN = (1901, 1, 20)
DATE_MAX = (2100, 12, 30)
ORDINAL_OFFSET = date(*DATE_MIN).toordinal() - 1

CCD_MIN = (1900, 12, 1, False)
CCD_MAX = (2100, 11, 30, False)
CCD_ORDINAL_MIN = 1  # ChineseCalendarDate.min.to_ordinal()
CCD_ORDINAL_MAX = 73029  # ChineseCalendarDate.max.to_ordinal()
CCD_INFO = {
    1900: 0x800,
    1901: 0x752, 1902: 0xea5, 1903: 0xab2a, 1904: 0x64b, 1905: 0xa9b,
    1906: 0x9aa6, 1907: 0x56a, 1908: 0xb59, 1909: 0x4baa, 1910: 0x752,
    1911: 0xcda5, 1912: 0xb25, 1913: 0xa4b, 1914: 0xba4b, 1915: 0x2ad,
    1916: 0x56b, 1917: 0x45b5, 1918: 0xda9, 1919: 0xfe92, 1920: 0xe92,
    1921: 0xd25, 1922: 0xad2d, 1923: 0xa56, 1924: 0x2b6, 1925: 0x9ad5,
    1926: 0x6d4, 1927: 0xea9, 1928: 0x4f4a, 1929: 0xe92, 1930: 0xc6a6,
    1931: 0x52b, 1932: 0xa57, 1933: 0xb956, 1934: 0xb5a, 1935: 0x6d4,
    1936: 0x7761, 1937: 0x749, 1938: 0xfb13, 1939: 0xa93, 1940: 0x52b,
    1941: 0xd51b, 1942: 0xaad, 1943: 0x56a, 1944: 0x9da5, 1945: 0xba4,
    1946: 0xb49, 1947: 0x4d4b, 1948: 0xa95, 1949: 0xeaad, 1950: 0x536,
    1951: 0xaad, 1952: 0xbaca, 1953: 0x5b2, 1954: 0xda5, 1955: 0x7ea2,
    1956: 0xd4a, 1957: 0x10595, 1958: 0xa97, 1959: 0x556, 1960: 0xc575,
    1961: 0xad5, 1962: 0x6d2, 1963: 0x8755, 1964: 0xea5, 1965: 0x64a,
    1966: 0x664f, 1967: 0xa9b, 1968: 0xeada, 1969: 0x56a, 1970: 0xb69,
    1971: 0xabb2, 1972: 0xb52, 1973: 0xb25, 1974: 0x8b2b, 1975: 0xa4b,
    1976: 0x10aab, 1977: 0x2ad, 1978: 0x56d, 1979: 0xd5a9, 1980: 0xda9,
    1981: 0xd92, 1982: 0x8e95, 1983: 0xd25, 1984: 0x14e4d, 1985: 0xa56,
    1986: 0x2b6, 1987: 0xc2f5, 1988: 0x6d5, 1989: 0xea9, 1990: 0xaf52,
    1991: 0xe92, 1992: 0xd26, 1993: 0x652e, 1994: 0xa57, 1995: 0x10ad6,
    1996: 0x35a, 1997: 0x6d5, 1998: 0xab69, 1999: 0x749, 2000: 0x693,
    2001: 0x8a9b, 2002: 0x52b, 2003: 0xa5b, 2004: 0x4aae, 2005: 0x56a,
    2006: 0xedd5, 2007: 0xba4, 2008: 0xb49, 2009: 0xad53, 2010: 0xa95,
    2011: 0x52d, 2012: 0x855d, 2013: 0xab5, 2014: 0x12baa, 2015: 0x5d2,
    2016: 0xda5, 2017: 0xde8a, 2018: 0xd4a, 2019: 0xc95, 2020: 0x8a9e,
    2021: 0x556, 2022: 0xab5, 2023: 0x4ada, 2024: 0x6d2, 2025: 0xc765,
    2026: 0x725, 2027: 0x64b, 2028: 0xa657, 2029: 0xcab, 2030: 0x55a,
    2031: 0x656e, 2032: 0xb69, 2033: 0x16f52, 2034: 0xb52, 2035: 0xb25,
    2036: 0xdd0b, 2037: 0xa4b, 2038: 0x4ab, 2039: 0xa2bb, 2040: 0x5ad,
    2041: 0xb6a, 2042: 0x4daa, 2043: 0xd92, 2044: 0xeea5, 2045: 0xd25,
    2046: 0xa55, 2047: 0xba4d, 2048: 0x4b6, 2049: 0x5b5, 2050: 0x76d2,
    2051: 0xec9, 2052: 0x10f92, 2053: 0xe92, 2054: 0xd26, 2055: 0xd516,
    2056: 0xa57, 2057: 0x556, 2058: 0x9365, 2059: 0x755, 2060: 0x749,
    2061: 0x674b, 2062: 0x693, 2063: 0xeaab, 2064: 0x52b, 2065: 0xa5b,
    2066: 0xaaba, 2067: 0x56a, 2068: 0xb65, 2069: 0x8baa, 2070: 0xb4a,
    2071: 0x10d95, 2072: 0xa95, 2073: 0x52d, 2074: 0xc56d, 2075: 0xab5,
    2076: 0x5aa, 2077: 0x85d5, 2078: 0xda5, 2079: 0xd4a, 2080: 0x6e4d,
    2081: 0xc96, 2082: 0xecce, 2083: 0x556, 2084: 0xab5, 2085: 0xbad2,
    2086: 0x6d2, 2087: 0xea5, 2088: 0x872a, 2089: 0x68b, 2090: 0x10697,
    2091: 0x4ab, 2092: 0x55b, 2093: 0xd556, 2094: 0xb6a, 2095: 0x752,
    2096: 0x8b95, 2097: 0xb45, 2098: 0xa8b, 2099: 0x4a4f, 2100: 0x4ab,
}


def _unzip_year(year):
    def _last_day(_month):
        return 30 if CCD_INFO[year] >> _month & 1 > 0 else 29

    if year == 1900:
        return {(12, False): _last_day(11)}
    if year == 2100:
        return {(_m, False): _last_day(_m) for _m in range(11)}

    if not (_leap := CCD_INFO[year] >> 13):
        return {(m + 1, False): _last_day(m) for m in range(12)}
    months = [((m + 1, False), _last_day(m)) for m in range(12)] + [((_leap, True), _last_day(12))]
    months.sort()
    return dict(months)


CCD_INFO = {_y: _unzip_year(_y) for _y in CCD_INFO}


def _check_date_fields(year: int, month: int, day: int, is_leap_month: bool):
    if not all(isinstance(v, int) for v in (year, month, day)):
        raise TypeError('year、month、day 必须是整数类型。')
    if is_leap_month not in (True, False):
        raise TypeError('is_leap_month 必须是布尔类型。')
    if not 1 <= month <= 12:
        raise ValueError('农历月只能是一个从 1 到 12 的整数。')
    if not 1 <= day <= 30:
        raise ValueError('农历日只能是一个从 1 到 30 的整数。')
    if not CCD_MIN <= (year, month, day, is_leap_month) <= CCD_MAX:
        raise OverflowError('超出精度范围。请使用更高精度的 Calendar。')

    try:
        days = CCD_INFO[year][(month, is_leap_month)]
    except KeyError:
        tip = '闰' if is_leap_month else ''
        raise ValueError(f'农历{year}年没有{tip}{month}月。')

    if day > days:
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
    def from_date(cls, _date: date):
        """将公历日期转换为农历日期。"""
        assert 0 < (n := _date.toordinal() - ORDINAL_OFFSET)
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
