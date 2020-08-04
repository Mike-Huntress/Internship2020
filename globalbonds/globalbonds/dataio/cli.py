
import click
import logging

from .constants import DATA_LIB_NAME, LOGGER_NAME
from .api import pull_and_write_streams


logging.basicConfig(
    level=logging.INFO,
    format="[%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(LOGGER_NAME)


@click.group('data')
def main():
    pass


@main.command('pull')
@click.option('-d', '--data-dir', default=DATA_LIB_NAME)
@click.argument('username')
@click.argument('password')
def pull_data(data_dir, username, password):
    logger.info('pulling data')
    pull_and_write_streams(username, password, data_dir=data_dir)
