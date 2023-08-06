from grid import rich_click
from grid.client import Grid


@rich_click.command()
def history() -> None:
    """View list of historic Runs."""
    client = Grid()
    client.history()
