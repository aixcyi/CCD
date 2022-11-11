try:
    import ephem
    from py_clc.ephemeris import ChineseCalendarDate, EphemCCD
except ImportError:
    from py_clc.base import ChineseCalendarDate

from py_clc.base import FastCCD

__version__ = '0.1.2'

if __name__ == '__main__':
    from datetime import date, timedelta

    ccd = ChineseCalendarDate.strptime('农历2020年闰四月廿九', '农历%Y年%b月%a')
    assert ccd.timetuple() == (2020, 4, 29, True)
    ccd = ChineseCalendarDate(2020, 4, 29, True)
    assert ccd.timetuple() == (2020, 4, 29, True)
    assert ccd.day_of_year == 148  # 这一天是当年的第148天
    assert ccd.days_in_year == 384  # 农历2020年总共384天（2020.1.25-2021.2.11）
    assert ccd.days_in_month == 29  # 农历2020年闰四月总共29天
    assert ccd.year_stem_branch == '庚子'
    assert ccd.year_zodiac == '鼠'
    assert ccd.month_ordinal == '闰四'
    assert ccd.day_ordinal == '廿九'
    assert str(ccd) == '农历2020年闰四月廿九'
    gcd = ccd.to_date()
    assert gcd == date(2020, 6, 20)
    ccd = ChineseCalendarDate.from_date(date(2020, 6, 20))
    assert ccd.timetuple() == (2020, 4, 29, True)

    today = ChineseCalendarDate(2020, 4, 29, True)
    tomorrow = today + timedelta(days=1)
    yesterday = today - timedelta(days=1)
    assert tomorrow.timetuple() == (2020, 5, 1, False)
    assert yesterday.timetuple() == (2020, 4, 28, True)
    assert today < tomorrow
    assert today > yesterday

    today2 = today + timedelta(days=0)
    assert today.timetuple() == today2.timetuple()
    assert id(today) != id(today2)
    today2 = today - timedelta(days=0)
    assert today.timetuple() == today2.timetuple()
    assert id(today) != id(today2)
