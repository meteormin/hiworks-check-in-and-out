import click
from attendance.definitions import PATH, TIMEZONE
from attendance.worker import Worker
from attendance.schedule import scheduler
from apscheduler.schedulers.background import BlockingScheduler
import config


def get_worker():
    """
    get worker object
    :return: worker object
    :rtype: Worker
    """
    return Worker(PATH)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkin(login_id: str = None, passwd: str = None):
    """
    check in
    :param login_id:
    :type login_id: str | None
    :param passwd:
    :type passwd: str | None
    :return:
    :rtype: int
    """
    return get_worker().checkin(login_id, passwd)


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    """
    check out
    :param login_id:
    :type login_id: str | None
    :param passwd:
    :type passwd: str | None
    :return:
    :rtype: int
    """
    return get_worker().checkout(login_id, passwd)


@cli.command()
def check_work_hour():
    """
    check your current work hour
    :return:
    """
    return get_worker().check_work_hour()


@cli.command()
def check_and_alert():
    """
    check your current work hour,
    if you work hour over 9 hour then send alert mail

    :return:
    """
    return get_worker().check_and_alert()


@cli.command()
@click.option('-m', '--month', required=False, type=click.types.INT, help='month')
@click.option('-y', '--year', required=False, type=click.types.INT, help='year')
def report_for_month(month: int = None, year: int = None):
    return get_worker().report_for_month(month, year)


@cli.command()
def sync_local_storages():
    get_worker().sync_local_storages()


@cli.command()
def test():
    return get_worker().test()


@cli.command()
def schedule():
    scheduler_config = config.SCHEDULER
    worker = get_worker()

    scheduler_config['sync-local-storages'] = {
        "func": "sync_local_storages",
        "args": [],
        "month": "*",
        "day": "*",
        "hour": "00",
        "minute": "00",
        "second": "00",
        "day_of_week": "mon-fri"
    }

    for k, v in scheduler_config.items():
        if v['func']:
            v['func'] = getattr(worker, v['func'])

    scheduler.register(BlockingScheduler(timezone=TIMEZONE), scheduler_config)


if __name__ == '__main__':
    cli()
