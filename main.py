import click
from browser.chrome import Chrome
from logger.log import Log
from utils.date import is_holidays
from configparser import ConfigParser
import os
import datetime


def config(file_path: str = 'hiworks.ini'):
    current_path = os.path.dirname(os.path.abspath(__file__))
    config_parser = ConfigParser()
    config_parser.read(os.path.join(current_path, file_path))
    return config_parser


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
    if login_id is None or passwd is None:
        conf = config()
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    browser = Chrome(Log.logger('checkin'))
    browser.checkin(login_id, passwd)

    return 0


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    if is_holidays(date=datetime.date.today()):
        return 1

    if login_id is None or passwd is None:
        conf = config()
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    browser = Chrome(Log.logger('checkout'))
    browser.checkout(login_id, passwd)

    return 0


if __name__ == '__main__':
    cli()
