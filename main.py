"""
TODO: write docstr
"""
import typer
from loguru import logger

from vk_fetch import core, fetchers, constants, utils

app = typer.Typer(name="vk_fetch", help=__doc__)


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
    logger.info("Provided params:")
    logger.info(f"  login:\t{login}")
    logger.info(f"  password:\t{password}")
    core.APIProvider.kate_mobile(login, password)


@app.command()
def show(
    login: str = typer.Option(
        ..., help="Login from VK account (e-mail/phone)"
    ),
    password: str = typer.Option(..., help="Password from VK account "),
) -> None:
    """
    Show all profile info to stdout
    """
    api = core.APIProvider.kate_mobile(login, password)
    permissions = fetchers.granted_permissions(api)
    logger.info("Granted permissions")
    logger.info(permissions)
    logger.info("---------------------------------")
    profile_info = fetchers.profile_info(api)
    logger.info("Fetched info")
    logger.info(profile_info)
    logger.info("---------------------------------")
    photos = fetchers.photos(api)
    logger.info("Fetched photos")
    for p in photos:
        logger.info(p)
    logger.info("---------------------------------")
    to_exclude = []
    convs = fetchers.conversations(api).excluded_peers(to_exclude)
    for peer_id in convs.peer_ids():
        logger.info(f"Fetched photos of conversation(peer_id={peer_id})")
        attachment_items = fetchers.conversation_attachments_iter(
            api, peer_id, constants.MediaType.Photo
        )
        for aitem in attachment_items:
            logger.info(aitem.attachment.photo.highest_quality())


if __name__ == "__main__":
    app()
