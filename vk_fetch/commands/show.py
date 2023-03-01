import pathlib

import rich.progress
import typer

from vk_fetch import constants, core, utils, fetchers, jobs

show_cmd = typer.Typer(name="show", help="Print available data of VK profile")


@show_cmd.command(name="conversations")
def show_conversation_attachments(
    sels: list[str] = typer.Argument(
        ...,
        help='List of conversation sel (e.g. "100000000" "-200000000" "c100" )',
        show_default=False,
    ),
    login: str = typer.Option(
        None, help="Login from VK account (e-mail/phone)", show_default=False
    ),
    password: str = typer.Option(
        None, help="Password from VK account", show_default=False
    ),
):
    """
    Show all attachments of conversations with sel
    """
    login = login or typer.prompt("Enter VK login")
    password = password or typer.prompt("Enter password", hide_input=True)
    api = core.APIProvider.kate_mobile(login, password)

    conversation_peer_ids = [utils.peer_id_from_sel(sel) for sel in sels]
    peer_ids = [
        pid
        for pid in fetchers.conversations(api).peer_ids()
        if pid in conversation_peer_ids
    ]
    media_types = constants.DEFAULT_CONVERSATION_MEDIA_TYPES

    to_execute = [
        (
            jobs.base.CheckPermissionsJob(api, silent=True),
            "Checking permissions...",
        ),
        *jobs.conversations.ShowConversationAttachmentsJob.batch_with_description(
            api, peer_ids, media_types
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


@show_cmd.command(name="all")
def show_all(
    login: str = typer.Option(
        None, help="Login from VK account (e-mail/phone)", show_default=False
    ),
    password: str = typer.Option(
        None, help="Password from VK account", show_default=False
    ),
) -> None:
    """
    Show all content of profile and all attachments of every conversation
    """
    login = login or typer.prompt("Enter VK login")
    password = password or typer.prompt("Enter password", hide_input=True)
    api = core.APIProvider.kate_mobile(login, password)

    peer_ids = [pid for pid in fetchers.conversations(api).peer_ids()]
    media_types = constants.DEFAULT_CONVERSATION_MEDIA_TYPES

    to_execute = [
        jobs.base.CheckPermissionsJob(api),
        jobs.profile.ShowProfileInfoJob(api),
        jobs.photos.ShowPhotosJob(api),
        *jobs.conversations.ShowConversationAttachmentsJob.batch_with_description(
            api, peer_ids, media_types
        ),
    ]
    jobs.run_all(to_execute)
