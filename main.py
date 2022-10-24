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
from utils.date import is_holidays, seconds_to_hours
from configparser import ConfigParser
from database.drivers.local import LocalSchema, LocalDriver
from definitions import PATH


def config(file_path: str = 'hiworks.ini'):
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

    conf = config()
    if login_id is None or passwd is None:
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    url = conf['default']['url']

    browser = get_browser('checkin', url)

    now = datetime.now()

    data = LocalSchema({
        'login_id': login_id,
        'checkin_at': now.strftime('%H:%M:%S'),
        'checkout_at': None,
        'work_hour': 0
    })

    data_store = LocalDriver(PATH['database'], data)

    browser.checkin(LoginData(login_id=login_id, login_pass=passwd), Checkin())

    if data_store.save(now.strftime('%Y-%m-%d'), data):
        return 0

    return 1


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    if is_holidays(date=date.today()):
        return 1

    conf = config()
    if login_id is None or passwd is None:
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    url = conf['default']['url']

    browser = get_browser('checkout', url)

    data = LocalSchema()

    data_store = LocalDriver(PATH['database'], data)

    now = datetime.now()

    data = data_store.get(now.strftime('%Y-%m-%d'))

    browser.checkout(LoginData(login_id=login_id, login_pass=passwd), Checkout())

    if data is not None:
        data.checkout_at = now.strftime('%H:%M:%S')

        in_time = time.strptime(data.checkout_at, '%H:%M:%S')
        out_time = time.strptime(data.checkin_at, '%H:%M:%S')

        data.work_hour = seconds_to_hours(time.mktime(in_time) - time.mktime(out_time))
        data_store.save(now.strftime('%Y-%m-%d'), data)

    return 0


if __name__ == '__main__':
    cli()
