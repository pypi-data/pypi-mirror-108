from pytz import timezone, utc, BaseTzInfo

from shuttl_time import WeekTime, WeekTimeWindow, MilitaryTimeWindow
from shuttl_time.military_time import MilitaryTime
from shuttl_time.weekday import WeekDay

time_zone_string = "Asia/Kolkata"
time_zone = timezone(time_zone_string)


def mt_in_time_zone(time: int, time_zone: timezone = time_zone) -> MilitaryTime:
    mt = MilitaryTime(time, time_zone)
    return mt


def mt_in_utc(time: int) -> MilitaryTime:
    return MilitaryTime(time, utc)


def week_time_dm(
    day_of_week: WeekDay = WeekDay.MONDAY,
    start_time: MilitaryTime = mt_in_time_zone(900),
) -> WeekTime:
    wt = WeekTime(day_of_week, start_time)
    return wt


def week_time_window_dm(start: WeekTime = None, end: WeekTime = None) -> WeekTimeWindow:
    start = start or week_time_dm()
    return WeekTimeWindow(start=start, end=end or start)


def military_time_window_dm(
    from_time: int = 1000, to_time: int = 1200, timezone: BaseTzInfo = utc
) -> MilitaryTimeWindow:
    return MilitaryTimeWindow(
        from_time=MilitaryTime(from_time, timezone),
        to_time=MilitaryTime(to_time, timezone),
    )
