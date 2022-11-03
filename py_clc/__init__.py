try:
    import ephem
    from py_clc.ephemeris import ChineseCalendarDate, EphemCCD
except ImportError:
    from py_clc.base import ChineseCalendarDate, FastCCD
