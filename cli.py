import click
from definitions import PATH
from worker import Worker
from apscheduler.schedulers.background import BlockingScheduler


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
def test():
    return get_worker().test()


@cli.command()
def schedule():
    scheduler = BlockingScheduler()

    scheduler.add_job(
        get_worker().test,
        'cron',
        id='scheduler',
        second='00',
        minute='*',
        hour='*',
        day_of_week='*'
    )

    scheduler.add_job(
        get_worker().checkin,
        'cron',
        id='scheduler.checkin',
        second='00',
        minute='00',
        hour='09',
        day_of_week='1-5'
    )

    scheduler.add_job(
        get_worker().checkout,
        'cron',
        id='scheduler.checkout',
        second='00',
        minute='00',
        hour='20',
        day_of_week='1-5'
    )

    scheduler.add_job(
        get_worker().check_and_alert,
        'cron',
        id='scheduler.checkout',
        second='00',
        minute='*/10',
        hour='08-22',
        day_of_week='1-5'
    )

    scheduler.start()


if __name__ == '__main__':
    cli()
