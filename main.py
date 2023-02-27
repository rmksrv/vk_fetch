"""
App for downloading data from VK
"""
import pathlib

import rich.progress
import typer

from vk_fetch import core, jobs, constants
from vk_fetch.logging import configure_logger, log

app = typer.Typer(name="vk_fetch", help=__doc__)
configure_logger()


@app.command()
def ping(
    login: str = typer.Option(
        ..., help="Login from VK account (e-mail/phone)"
    ),
    password: str = typer.Option(..., help="Password from VK account "),
) -> None:
    """
    Check app can connect to VK and auth as user with login/pass
    """
    log("Provided params:")
    log(f"  login:\t{login}")
    log(f"  password:\t{password}")
    api = core.APIProvider.kate_mobile(login, password)
    jobs.base.CheckPermissionsJob(api).run()


@app.command()
def show(
    login: str = typer.Option(
        ..., help="Login from VK account (e-mail/phone)"
    ),
    password: str = typer.Option(..., help="Password from VK account "),
) -> None:
    """
    Show all profile info
    """
    api = core.APIProvider.kate_mobile(login, password)
    to_execute = [
        jobs.base.CheckPermissionsJob(api),
        jobs.profile.ShowProfileJob(api),
        jobs.photos.ShowPhotosJob(api),
    ]
    jobs.run_all(to_execute)


@app.command()
def download(
    login: str = typer.Option(
        ..., help="Login from VK account (e-mail/phone)"
    ),
    password: str = typer.Option(..., help="Password from VK account "),
    destination: pathlib.Path = typer.Option(
        default=constants.DEFAULT_DESTINATION_PATH,
        help="Path where all fetched data will be written",
    ),
) -> None:
    """
    Download all data and media of VK profile
    """
    destination = pathlib.Path(destination)
    photos_destination = destination / "photos"
    api = core.APIProvider.kate_mobile(login, password)
    to_execute = [
        (
            jobs.base.CheckPermissionsJob(api, silent=True),
            "Checking permissions...",
        ),
        (
            jobs.photos.DownloadPhotosJob(api, photos_destination),
            "Downloading photos...",
        ),
    ]
    for job, description in to_execute:
        with rich.progress.Progress(
            rich.progress.SpinnerColumn(),
            rich.progress.TextColumn(
                "[progress.description]{task.description}"
            ),
            transient=True,
        ) as progress:
            progress.add_task(description=description, total=None)
            job.run()


if __name__ == "__main__":
    app()
