try:
    import ephem
    from py_clc.calc_ephem import ChineseCalendarDate
except ImportError:
    from py_clc.limited import ChineseCalendarDate
