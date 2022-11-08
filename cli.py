import click
from definitions import PATH
from worker import Worker


def get_worker():
    return Worker(PATH)


@click.group()
def cli():
    pass


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkin(login_id: str = None, passwd: str = None):
    return get_worker().checkin(login_id, passwd)


@cli.command()
@click.option('--login_id', required=False, type=click.types.STRING, help='hiworks id')
@click.option('--passwd', required=False, type=click.types.STRING, help='hiworks password')
def checkout(login_id: str = None, passwd: str = None):
    return get_worker().checkout(login_id, passwd)


@cli.command()
def check_work_hour():
    return get_worker().check_work_hour()


@cli.command()
def check_and_alert():
    return get_worker().check_and_alert()


@cli.command()
def test():
    return get_worker().test()


if __name__ == '__main__':
    cli()
