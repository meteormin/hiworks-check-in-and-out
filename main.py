import click
from browser.chrome import Chrome
from logger.log import Log
from configparser import ConfigParser
import os


def config(file_path: str = 'hiworks.ini'):
    current_path = current_path = os.path.dirname(os.path.abspath(__file__))
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
    if login_id is None or passwd is None:
        conf = config()
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    browser = Chrome(Log.logger('checkin'))
    browser.checkin(login_id, passwd)


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    if login_id is None or passwd is None:
        conf = config()
        login_id = conf['default']['id']
        passwd = conf['default']['password']

    browser = Chrome(Log.logger('checkout'))
    browser.checkout(login_id, passwd)


if __name__ == '__main__':
    cli()
