from pytimekr import pytimekr
import datetime


def is_holidays(date: datetime.date = None):
    if date is None:
        date = datetime.date.today()

    holidays = pytimekr.holidays()

    if date in holidays:
        return True

    return False


def seconds_to_hours(seconds: float) -> str:
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)
