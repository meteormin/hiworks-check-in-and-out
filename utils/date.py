from pytimekr import pytimekr
import datetime


def is_holidays(date: datetime.date = None):
    if date is None:
        date = datetime.date.today()

    holidays = pytimekr.holidays()

    if date in holidays:
        return True

    return False
