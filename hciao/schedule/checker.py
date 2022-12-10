from datetime import datetime
from hciao.database.drivers.abstracts import Driver
from hciao.database.drivers.local import LocalSchema
from hciao.utils.date import get_last_day_of_month, hours_to_seconds
from hciao.definitions import WORK_HOURS
from dataclasses import dataclass
import time


@dataclass()
class WorkTime:
    checkin_at: float
    work: float
    left: float
    acc: float
    avg: float


class Checker:

    def __init__(self, data_store: Driver):
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
                checkin_at=float(hours_to_seconds(data.checkin_at)),
                work=float(hours_to_seconds(work_time)),
                left=0.0,
                acc=0.0,
                avg=0.0
            )
        else:
            now = datetime.now()
            now_time = time.strptime(now.strftime('%H:%M:%S'), '%H:%M:%S')
            in_time = time.strptime(data.checkin_at, '%H:%M:%S')
            work_seconds = time.mktime(now_time) - time.mktime(in_time)

            return WorkTime(
                checkin_at=float(time.mktime(in_time)),
                work=float(work_seconds),
                left=float(WORK_HOURS * 3600) - work_seconds,
                acc=0.0,
                avg=0.0
            )

    def get_work_hour_today(self) -> WorkTime | None:
        now = datetime.now()
        return self.get_work_hour(now.strftime('%Y-%m-%d'))

    def get_work_hours_month(self, month: int = None, year: int = None) -> list[WorkTime | None]:
        today = datetime.today()
        if year is None or year < 0:
            year = today.year
        if month is None or month < 0:
            month = today.month
        today_time = time.mktime(time.strptime(today.strftime('%Y-%m-%d'), '%Y-%m-%d'))

        work_hours = []
        acc = 0
        for day in range(1, get_last_day_of_month(month, year)):
            date_id = f"{year}-{str(month).zfill(2)}-{str(day).zfill(2)}"
            date_id_time = time.mktime(time.strptime(date_id, '%Y-%m-%d'))

            if (today_time - date_id_time) < 0:
                break

            work_time = self.get_work_hour(date_id)

            if work_time is not None:
                acc += work_time.work
                avg = acc / (len(work_hours) + 1)
                work_time.acc = acc
                work_time.avg = avg

                work_hours.append(work_time)

        return work_hours
