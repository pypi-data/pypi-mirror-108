from typing import List

from grid import rich_click
from grid.client import Grid


@rich_click.group()
def cancel() -> None:
    pass


@cancel.command()
@rich_click.argument('experiment_ids', type=str, required=True, nargs=-1)
def experiment(experiment_ids: List[str]):
    client = Grid()
    for experiment in experiment_ids:
        client.cancel(experiment_name=experiment)


@cancel.command()
@rich_click.argument('run_ids', type=str, required=True, nargs=-1)
def run(run_ids: List[str]):
    client = Grid()
    for run in run_ids:
        client.cancel(run_name=run)
