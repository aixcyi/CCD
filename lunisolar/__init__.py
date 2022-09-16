try:
    import skyfield
    from lunisolar.chinese.calculated import ChineseCalendarDate
except ImportError:
    from lunisolar.chinese.limited import ChineseCalendarDate
