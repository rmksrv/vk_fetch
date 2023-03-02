import pathlib

import rich.progress
import typer

from src import constants, utils, core, fetchers, jobs, models

download_cmd = typer.Typer(
    name="download", help="Download data from VK profile"
)


@download_cmd.command(name="conversations")
def download_conversation_attachments(
    sels: list[str] = typer.Argument(
        ...,
        help='List of conversation sel (e.g. "100000000" "-200000000" "c100" )',
        show_default=False,
    ),
    login: str = typer.Option(
        None, help="Login from VK account (e-mail/phone)"
    ),
    password: str = typer.Option(None, help="Password from VK account"),
    destination: pathlib.Path = typer.Option(
        default=constants.DEFAULT_DESTINATION_PATH,
        help="Path where all fetched data will be written",
    ),
):
    """
    Download all attachments of conversations with sel
    """
    login = login or typer.prompt("Enter VK login")
    password = password or typer.prompt("Enter password", hide_input=True)
    api = core.APIProvider.kate_mobile(login, password)

    conversation_peer_ids = [utils.peer_id_from_sel(sel) for sel in sels]
    conversation_items = models.ConversationItemList(
        [
            conv
            for conv in fetchers.conversation_items(api)
            if conv.conversation.peer.id in conversation_peer_ids
        ]
    )
    media_types = constants.DEFAULT_CONVERSATION_MEDIA_TYPES

    to_execute = [
        (
            jobs.base.CheckPermissionsJob(api, silent=True),
            "Checking permissions...",
        ),
        *jobs.conversations.DownloadConversationAttachmentsJob.batch_with_description(
            api, conversation_items, destination, media_types
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


@download_cmd.command(name="all")
def download_all(
    login: str = typer.Option(
        None, help="Login from VK account (e-mail/phone)"
    ),
    password: str = typer.Option(None, help="Password from VK account"),
    destination: pathlib.Path = typer.Option(
        default=constants.DEFAULT_DESTINATION_PATH,
        help="Path where all fetched data will be written",
    ),
    exclude_sels: str = typer.Option(
        None,
        help="List of sels attachments of which won't be downloaded. "
        "NOTE: Separate sels with space and wrap list. "
        'E.g.: "11111111 -20000000 c100"',
    ),
) -> None:
    """
    Download all content of profile and all attachments of every conversation
    """
    login = login or typer.prompt("Enter VK login")
    password = password or typer.prompt("Enter password", hide_input=True)
    api = core.APIProvider.kate_mobile(login, password)

    exclude_peer_ids = [
        utils.peer_id_from_sel(sel) for sel in exclude_sels.split()
    ]
    photos_destination = destination / "photos"
    attachments_destination = destination / "attachments"
    conversation_items = models.ConversationItemList(
        [
            conv
            for conv in fetchers.conversation_items(api)
            if conv.conversation.peer.id not in exclude_peer_ids
        ]
    )
    media_types = constants.DEFAULT_CONVERSATION_MEDIA_TYPES

    to_execute = [
        (
            jobs.base.CheckPermissionsJob(api, silent=True),
            "Checking permissions...",
        ),
        (
            jobs.photos.DownloadPhotosJob(api, photos_destination),
            "Downloading photos...",
        ),
        *jobs.conversations.DownloadConversationAttachmentsJob.batch_with_description(
            api, conversation_items, attachments_destination, media_types
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
