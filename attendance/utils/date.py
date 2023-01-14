import datetime
import calendar
from pytimekr import pytimekr

weekend = [5, 6]


def is_holidays(date: datetime.date = None, with_weekend: bool = True):
    if date is None:
        date = datetime.date.today()

    holidays = pytimekr.holidays()

    if date in holidays:
        return True

    if with_weekend:
        weekday = date.weekday()
        if weekday in weekend:
            return True

    return False


def seconds_to_hours(seconds: float) -> str:
    if seconds < 0:
        prev_ch = '-'
    else:
        prev_ch = '+'

    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return f"{prev_ch}%d:%02d:%02d" % (hour, minutes, seconds)


def hours_to_seconds(hours: str) -> float:
    [hour, minutes, seconds] = hours.split(':')
    hs = int(hour) * 3600
    ms = int(minutes) * 60
    return int(seconds) + ms + hs


def get_last_day_of_month(month: int, year: int = None) -> int:
    if year is None or year < 0:
        year = datetime.datetime.now().year

    month_range = calendar.monthrange(year, month)

    return month_range[-1]
