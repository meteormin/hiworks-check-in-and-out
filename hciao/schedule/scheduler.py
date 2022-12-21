import dataclasses
import os
import time
from apscheduler.schedulers.base import BaseScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from hciao.logger.log import Log
from hciao.utils.object import map_from_dict


@dataclasses.dataclass
class JobArgument:
    job_id: str | None = None
    func: callable = None
    args: list | None = None
    month: str | None = None
    day: str | None = None
    hour: str | None = None
    minute: str | None = None
    second: str | None = None
    day_of_week: str | None = None


def register(s: BaseScheduler, config: dict):
    logger = Log.logger('scheduler')

    def _add_job(job: JobArgument):
        logger.info(f"add_job: {job.job_id}")

        s.add_job(
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

    def _validate_job(job: dict) -> JobArgument | None:
        args = JobArgument()

        for key in job.keys():
            if key not in args.__dict__.keys():
                return None

        return map_from_dict(args, job)

    for s_id, job_dict in config.items():
        job_args = _validate_job(job_dict)
        if job_args is not None:
            job_args.job_id = s_id
            _add_job(job_args)
        else:
            logger.error(f"failed add job: {s_id}")

    logger.info('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

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