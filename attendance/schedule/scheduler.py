import dataclasses
import os
import time
from typing import Callable
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from attendance.logger.log import Log
from attendance.logger.logger_adapter import LoggerAdapter
from attendance.utils.object import map_from_dict


@dataclasses.dataclass
class JobArgument:
    job_id: str | None = None
    func: Callable[[], any] | None = None
    args: list | None = None
    month: str | None = None
    day: str | None = None
    hour: str | None = None
    minute: str | None = None
    second: str | None = None
    day_of_week: str | None = None


class Scheduler:
    _TAG: str = 'scheduler'

    def __init__(self, s: BaseScheduler, config: dict):
        self.logger = Log.logger(self._TAG)
        self.logger.info('init...')
        self.scheduler = s
        self.config = config

    def add_job(self, job: JobArgument):
        self.logger.info(f"add_job: {job.job_id}")
        self.scheduler.add_job(
            id=job.job_id,
            func=job.func,
            trigger='cron',
            month=job.month,
            day=job.day,
            hour=job.hour,
            minute=job.minute,
            second=job.second,
            day_of_week=job.day_of_week,
            args=job.args
        )

    @staticmethod
    def validate_job(job: dict):
        args = JobArgument()

        for key in job.keys():
            if key not in args.__dict__.keys():
                return None

        return map_from_dict(args, job)


def register(s: BaseScheduler, config: dict):
    def _health_check(logger: LoggerAdapter) -> bool:
        logger.info("health-check")
        return True

    scheduler = Scheduler(s, config)
    scheduler.add_job(JobArgument(
        job_id="health-check",
        func=_health_check,
        args=[scheduler.logger],
        month="*",
        day="*",
        hour="*",
        minute="*/5",
        second="00",
        day_of_week="mon-fri"
    ))

    for s_id, job_dict in config.items():
        job_args = scheduler.validate_job(job_dict)
        if job_args is not None:
            job_args.job_id = s_id
            scheduler.add_job(job_args)
        else:
            scheduler.logger.error(f"failed add job: {s_id}")

    scheduler.logger.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    if isinstance(s, BlockingScheduler):
        try:
            s.start()
        except (KeyboardInterrupt, SystemExit):
            pass
    elif isinstance(s, BackgroundScheduler):
        s.start()
        try:
            # This is here to simulate application activity (which keeps the main thread alive).
            while True:
                time.sleep(2)
        except (KeyboardInterrupt, SystemExit):
            # Not strictly necessary if daemonic mode is enabled but should be done if possible
            s.shutdown()
