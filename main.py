import click
import os
import time
from datetime import datetime, date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from browser.chrome import Chrome
from browser.hiworks.elements import Checkin, Checkout
from browser.login_data import LoginData
from logger.log import Log
from mailer.mailer import SimpleMailer
from schedule.checker import Checker
from utils.date import is_holidays, seconds_to_hours
from configparser import ConfigParser
from database.drivers.local import LocalSchema, LocalDriver
from definitions import PATH


def config(file_path: str):
    current_path = os.path.dirname(os.path.abspath(__file__))
    config_parser = ConfigParser()
    config_parser.read(os.path.join(current_path, file_path))
    return config_parser


def get_browser(tag: str, url: str):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    service = Service(ChromeDriverManager().install())

    return Chrome(
        Log.logger(tag),
        webdriver.Chrome(service=service, options=options),
        url
    )


def get_logger(tag: str):
    return Log.logger(tag)


def get_local_storage(path: str) -> LocalDriver:
    data = LocalSchema()
    return LocalDriver(path, data)


def get_mailer(mail_config: dict) -> SimpleMailer:
    return SimpleMailer(
        host=mail_config['outlook']['url'],
        login_id=mail_config['outlook']['id'],
        login_pass=mail_config['outlook']['password']
    )


@click.group()
def cli():
    pass


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkin(login_id: str = None, passwd: str = None):
    if is_holidays(date=date.today()):
        click.echo('today is holiday')
        return 1

    conf = config('hiworks.ini')
    if login_id is None or passwd is None:
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    url = conf['default']['url']

    browser = get_browser('checkin', url)
    check_time = browser.checkin(LoginData(login_id=login_id, login_pass=passwd), Checkin())

    now = datetime.now()
    data_store = get_local_storage(PATH['database'])

    data = data_store.data
    data.login_id = login_id
    data.checkout_at = None
    data.work_hour = None

    if check_time is None and check_time == '00:00:00':
        data.checkin_at = now.strftime('%Y-%m-%d')
    else:
        data.checkin_at = check_time

    if data_store.save(now.strftime('%Y-%m-%d'), data):
        return 0

    return 1


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    if is_holidays(date=date.today()):
        return 1

    conf = config('hiworks.ini')
    if login_id is None or passwd is None:
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    url = conf['default']['url']

    browser = get_browser('checkout', url)
    check_time = browser.checkout(LoginData(login_id=login_id, login_pass=passwd), Checkout())

    data_store = get_local_storage(PATH['database'])

    now = datetime.now()
    data = data_store.get(now.strftime('%Y-%m-%d'))

    if data is not None:
        if check_time is None and check_time == '00:00:00':
            data.checkout_at = now.strftime('%H:%M:%S')
        else:
            data.checkout_at = check_time

        out_time = time.strptime(data.checkout_at, '%H:%M:%S')
        in_time = time.strptime(data.checkin_at, '%H:%M:%S')

        data.work_hour = seconds_to_hours(time.mktime(out_time) - time.mktime(in_time))
        data_store.save(now.strftime('%Y-%m-%d'), data)

    return 0


@cli.command()
def check_work_hour():
    now = datetime.now()

    data_store = get_local_storage(PATH['database'])
    data = data_store.get(now.strftime('%Y-%m-%d'))

    if data.checkin_at is None:
        click.echo('not yet checkin')
        return 1

    if data.work_hour is not None:
        click.echo(f"already checkout: {data.checkout_at}")
        click.echo(f"work hours: {data.work_hour}")
    else:
        checker = Checker(data_store)
        work = checker.get_work_hour_today()
        click.echo(f"work hours: {seconds_to_hours(work['work'])}")

        if work['left'] < 0:
            click.echo(f"left hours: {seconds_to_hours(work['left'])}")
        else:
            click.echo(f"over hours: {seconds_to_hours(work['left'])}")
    return 0


@cli.command()
def check_and_alert():
    now = datetime.now()

    data_store = get_local_storage(PATH['database'])
    data = data_store.get(now.strftime('%Y-%m-%d'))
    logger = get_logger('check-and-alert')

    mail_config = config('mailer.ini')
    mailer = get_mailer(mail_config)

    if data.checkin_at is None:
        click.echo('not yet checkin')
        logger.debug('not yet checkin')
        hiworks = config('hiworks.ini')

        mailer.send(mail_config['outlook']['id'], f"[Alert] You Don't Checkin...", f"go: {hiworks['url']}")
        return 1

    if data.work_hour is not None:
        click.echo(f"already checkout: {data.checkout_at}")
        click.echo(f"work hours: {data.work_hour}")

        logger.debug(f"already checkout: {data.checkout_at}")
        logger.info(f"work hours: {data.work_hour}")
    else:
        checker = Checker(data_store)
        work = checker.get_work_hour_today()
        click.echo(f"work hours: {seconds_to_hours(work['work'])}")
        logger.info(f"work hours: {seconds_to_hours(work['work'])}")
        if work['left'] < 0:
            click.echo(f"left hours: {seconds_to_hours(work['left'])}")
            logger.info(f"left hours: {seconds_to_hours(work['left'])}")
            logger.debug(f"already checkout: {data.checkout_at}")
        else:
            click.echo(f"over hours: {seconds_to_hours(work['left'])}")
            logger.info(f"over hours: {seconds_to_hours(work['left'])}")
            if work['left'] <= 600:
                logger.debug(f"you must checkout!!")

                mailer.send(mail_config['outlook']['id'], '[Alert] You must checkout!!',
                            f"You must checkout, left {seconds_to_hours(work['left'])}")
    return 0


if __name__ == '__main__':
    cli()
