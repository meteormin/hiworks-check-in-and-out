import click
import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from browser.chrome import Chrome
from browser.hiworks.elements import Checkin, Checkout
from browser.login_data import LoginData
from logger.log import Log
from utils.date import is_holidays
from configparser import ConfigParser


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
    if is_holidays(date=datetime.date.today()):
        click.echo('today is holiday')
        return 1

    conf = config()
    if login_id is None or passwd is None:
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    url = conf['default']['url']

    browser = get_browser('checkin', url)
    browser.checkin(LoginData(login_id=login_id, login_pass=passwd), Checkin())

    return 0


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    if is_holidays(date=datetime.date.today()):
        return 1

    conf = config()
    if login_id is None or passwd is None:
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    url = conf['default']['url']

    browser = get_browser('checkout', url)
    browser.checkout(LoginData(login_id=login_id, login_pass=passwd), Checkout())

    return 0


if __name__ == '__main__':
    cli()
