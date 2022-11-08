from database.drivers.abstracts import Driver
from datetime import datetime
from definitions import WORK_HOURS
import time
from typing import Union, Dict


class Checker:

    def __init__(self, data_store: Driver):
        self.data_store = data_store

    def get_work_hour_today(self) -> Union[Dict[str, float], None]:
        now = datetime.now()
        data = self.data_store.get(now.strftime('%Y-%m-%d'))

        if data.checkin_at is None:
            return None

        if data.work_hour is not None:
            return None
        else:
            now_time = time.strptime(now.strftime('%H:%M:%S'), '%H:%M:%S')
            in_time = time.strptime(data.checkin_at, '%H:%M:%S')
            work_seconds = time.mktime(now_time) - time.mktime(in_time)
            return {
                'work': work_seconds,
                'left': float(WORK_HOURS * 3600) - work_seconds
            }
