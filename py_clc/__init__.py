try:
    import ephem
    from py_clc.ephemeris import ChineseCalendarDate
except ImportError:
    from py_clc.base import ChineseCalendarDate
