from pathlib import Path
from typing import List, Optional

import click
from rich.progress import BarColumn, Progress, SpinnerColumn, TimeRemainingColumn

from grid import rich_click
from grid.core import Artifact, Experiment, Run
from grid.downloader import DownloadableObject, Downloader
from grid.utilities import is_experiment


def _download_artifacts(artifacts: List[Artifact], download_dir: str) -> None:
    """
    Downloads a set of artifacts from Grid.

    Parameters
    ----------
    artifacts: List[Artifact]
        List of Artifact objects.

    download_dir: str
        Download directory for artifacts
    """
    # Create host directory.
    Downloader.create_dir_tree(dest_dir=download_dir)

    # Create downloadable objects.
    files_to_download = []
    for artifact in artifacts:
        files_to_download.append(
            DownloadableObject(url=artifact.url, download_path=artifact.path, filename=artifact.filename)
        )

    # Start download if there are any files to download.
    if files_to_download:
        D = Downloader(downloadable_objects=files_to_download, base_dir=download_dir)
        D.download()


@rich_click.command()
@click.option(
    "--download_dir",
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
    required=False,
    default="./grid_artifacts",
    help="Download directory that will host all artifact files."
)
@rich_click.argument(
    "runs_or_experiments", type=str, required=True, nargs=-1, help="The run or experiment to download artifacts for."
)
def artifacts(runs_or_experiments: List[str], download_dir: Optional[str] = None) -> None:
    """Downloads artifacts for a given run or experiments."""
    progress = Progress(
        SpinnerColumn(),
        "[progress.description]{task.fields[file]}",
        BarColumn(),
        "[progress.percentage]{task.percentage:>3.0f}%",
        TimeRemainingColumn(),
    )
    task = progress.add_task("downloading", total=len(runs_or_experiments), start=True, file="")

    click.echo(f"Downloading artifacts → {runs_or_experiments}")
    with progress:
        for element in runs_or_experiments:
            progress.tasks[task].fields["file"] = element
            if is_experiment(element):
                experiment = Experiment(name=element)
                experiment.refresh()
                _download_artifacts(experiment.artifacts, download_dir=download_dir)
                progress.update(task, advance=1)
            else:
                # Runs need their own host directory to make
                # it different than experiments.
                host_path = Path(download_dir) / Path(element)
                run = Run(identifier=element)

                for experiment in run.experiments:
                    progress.tasks[task].fields["file"] = element
                    experiment.refresh()
                    _download_artifacts(experiment.artifacts, download_dir=host_path)

                progress.update(task, advance=1)
