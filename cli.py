import click
import os
import json
from hciao.definitions import PATH, TIMEZONE
from hciao.worker import Worker
from hciao.schedule import scheduler
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
    with open(os.path.join(PATH["config"], 'scheduler.json')) as f:
        json_dict = json.load(f)

    parse_dict = {}
    worker = get_worker()
    for k, v in json_dict.items():
        parse_dict[k] = {}
        if v['command']:
            parse_dict[k]['func'] = getattr(worker, v['command'])

            del v['command']

            parse_dict[k].update(v)

    scheduler.register(BlockingScheduler(timezone=TIMEZONE), parse_dict)


if __name__ == '__main__':
    cli()
