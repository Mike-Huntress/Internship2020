
import click

from .dataio.cli import main as dataio_main


@click.group()
def main():
    pass


main.add_command(dataio_main)
