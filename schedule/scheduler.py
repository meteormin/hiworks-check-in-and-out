from apscheduler.schedulers.base import BaseScheduler

from logger.log import Log


def register(s: BaseScheduler, config: dict):
    logger = Log.logger('scheduler')

    def _add_job(_id: str, func, args: list, second: str, minute: str, hour: str, day_of_week: str):
        logger.info(f"add_job: {_id}")

        s.add_job(
            id=_id,
            func=func,
            trigger='cron',
            second=second,
            minute=minute,
            hour=hour,
            day_of_week=day_of_week,
            args=args
        )

    def _validate_job(job: dict):
        valid_keys = ['func', 'second', 'minute', 'hour', 'day_of_week', 'args']

        for key in job.keys():
            if key not in valid_keys:
                return False

        return True

    for s_id, job_dict in config.items():
        if _validate_job(job_dict):
            _add_job(s_id, **job_dict)
        else:
            logger.error(f"failed add job: {s_id}")

    s.start()
