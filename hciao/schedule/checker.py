from datetime import datetime
from hciao.storage.drivers.abstracts import Driver
from hciao.storage.drivers.local import LocalSchema
from hciao.utils.date import get_last_day_of_month, hours_to_seconds, seconds_to_hours
from hciao.definitions import WORK_HOURS
from dataclasses import dataclass
import time


@dataclass()
class WorkTime:
    checkin_at: str
    work: str
    left: str


class WorkHourStats:
    year: int
    month: int
    days: int
    acc: str
    avg: str


class Checker:

    def __init__(self, data_store: Driver):
        self.data_store = data_store

    def set_driver(self, data_store: Driver):
        self.data_store = data_store

    def get_work_hour(self, date_id: str) -> WorkTime | None:
        data = LocalSchema()

        data = self.data_store.get(data, date_id)

        if data is None:
            return None

        if data.checkin_at is None:
            return None

        if data.work_hour is not None:
            work_time = data.work_hour.replace('+', '')
            work_time = work_time.replace('-', '')

            return WorkTime(
                checkin_at=data.checkin_at,
                work=work_time,
                left="00:00:00",
            )
        else:
            now = datetime.now()
            now_time = time.strptime(now.strftime('%H:%M:%S'), '%H:%M:%S')
            in_time = time.strptime(data.checkin_at, '%H:%M:%S')
            work_seconds = time.mktime(now_time) - time.mktime(in_time)

            return WorkTime(
                checkin_at=data.checkin_at,
                work=seconds_to_hours(work_seconds),
                left=seconds_to_hours(float(WORK_HOURS * 3600) - work_seconds),
            )

    def get_work_hour_today(self) -> WorkTime | None:
        now = datetime.now()
        return self.get_work_hour(now.strftime('%Y-%m-%d'))

    def get_work_hours_month(self, month: int = None, year: int = None) -> WorkHourStats:
        today = datetime.today()
        if year is None or year < 0:
            year = today.year
        if month is None or month < 0:
            month = today.month
        today_time = time.mktime(time.strptime(today.strftime('%Y-%m-%d'), '%Y-%m-%d'))

        work_hour = WorkHourStats()

        work_hour.year = year
        work_hour.month = month
        work_hour.days = 0
        acc = 0
        for day in range(1, get_last_day_of_month(month, year)):
            date_id = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            date_id_time = time.mktime(time.strptime(date_id, '%Y-%m-%d'))

            if (today_time - date_id_time) < 0:
                break

            work_time = self.get_work_hour(date_id)

            if work_time is not None:
                acc += hours_to_seconds(work_time.work)
                work_hour.days += 1

        work_hour.acc = seconds_to_hours(acc)
        work_hour.avg = seconds_to_hours(acc / work_hour.days)

        return work_hour
