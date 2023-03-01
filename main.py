"""
Script helps to fetch all data from your VK account
"""

import typer

from vk_fetch import core, jobs, commands
from vk_fetch.logging import configure_logger, log


app = typer.Typer(name="vk_fetch", help=__doc__)
app.add_typer(commands.download_cmd)
app.add_typer(commands.show_cmd)
configure_logger()


@app.command()
def ping(
    login: str = typer.Option(
        None, help="Login from VK account (e-mail/phone)", show_default=False
    ),
    password: str = typer.Option(None, help="Password from VK account"),
) -> None:
    """
    Check app can connect to VK and auth as user with login/pass
    """
    login = login or typer.prompt("Enter VK login")
    password = password or typer.prompt("Enter password", hide_input=True)
    log("Provided params:")
    log(f"  login:\t{login}")
    log(f"  password:\t{password}")
    api = core.APIProvider.kate_mobile(login, password)
    jobs.base.CheckPermissionsJob(api).run()


if __name__ == "__main__":
    app()
