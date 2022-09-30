try:
    import ephem
    from lunisolar.chinese.calc_ephem import ChineseCalendarDate
except ImportError:
    from lunisolar.chinese.limited import ChineseCalendarDate
