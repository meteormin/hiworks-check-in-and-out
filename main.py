import click
from browser.chrome import Chrome
from logger.log import Log


@click.group()
def cli():
    pass


@cli.command()
@click.option('--id', required=True, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=True, type=click.types.STRING, help='hiworks password')
def checkin(_id: str, passwd: str):
    browser = Chrome(Log.logger('checkin'))
    browser.checkin(_id, passwd)


@cli.command()
@click.option('--id', required=True, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=True, type=click.types.STRING, help='hiworks password')
def checkout(_id: str, passwd: str):
    browser = Chrome(Log.logger('checkout'))
    browser.checkout(_id, passwd)


if __name__ == '__main__':
    cli()
