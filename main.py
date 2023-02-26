import typer
from loguru import logger

from vk_fetch import core, fetchers

app = typer.Typer()


@app.command()
def ping(
    login: str = typer.Option(..., help="Login from VK account (e-mail/phone)"),
    password: str = typer.Option(..., help="Password from VK account "),
    token: str = typer.Option(..., help="VK App token")
) -> None:
    """
    Check app can connect to VK and auth as user with login/pass
    """
    logger.info("Provided params:")
    logger.info(f"  login:\t{login}")
    logger.info(f"  password:\t{password}")
    logger.info(f"  token:\t{token}")
    core.new_api(login, password, token)


@app.command()
def show(
    login: str = typer.Option(..., help="Login from VK account (e-mail/phone)"),
    password: str = typer.Option(..., help="Password from VK account "),
    token: str = typer.Option(..., help="VK App token")
) -> None:
    """
    Show all profile info to stdout
    """
    api = core.new_api(login, password, token)
    profile_info = fetchers.profile_info(api)
    logger.info("Fetched info")
    logger.info(profile_info)
    photos = fetchers.photos(api)
    logger.info(photos)


if __name__ == "__main__":
    app()
