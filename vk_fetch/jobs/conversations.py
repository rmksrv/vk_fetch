import pathlib
import typing as t

from vk_fetch import core, constants, fetchers
from vk_fetch.jobs import base
from vk_fetch.logging import log


class DownloadConversationAttachmentsJob(base.VkFetchJob):
    def __init__(
        self,
        api: core.APIProvider,
        peer_id: int,
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ):
        super().__init__(api)
        self.peer_id = peer_id
        self.destination = destination
        self.media_types = media_types

    def run(self) -> None:
        counter = 0
        duplicate_counter = 0
        downloaded_hashes = set()
        if constants.MediaType.Audio in self.media_types:
            log(
                "  Downloading audio is still in development - skip it",
                level="WARNING",
            )
            # continue
        for media_type in self.media_types:
            for attachment_item in fetchers.conversation_attachments_iter(
                self.api, self.peer_id, media_type
            ):
                attachment_content = attachment_item.attachment.content()
                attachment_hash = hash(attachment_content)
                if attachment_hash in downloaded_hashes:
                    duplicate_counter += 1
                    continue
                log(
                    f"  Processing {attachment_content} from message at {attachment_item.date}"
                )
                downloaded_hashes.add(attachment_hash)
                counter += 1
        log(f"  Downloaded {counter} items from conversation")
        if duplicate_counter:
            log(f"  ({duplicate_counter}/{counter} duplicates)")

    @classmethod
    def batch(
        cls,
        api: core.APIProvider,
        peer_ids: list[int],
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ) -> list[t.Self]:
        return [
            cls(api, peer_id, destination, media_types) for peer_id in peer_ids
        ]

    @classmethod
    def batch_with_description(
        cls,
        api: core.APIProvider,
        peer_ids: list[int],
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ) -> list[tuple[t.Self, str]]:
        batch = cls.batch(api, peer_ids, destination, media_types)
        descriptions = [
            f"Downloading attachments of conversation with peer(id={peer_id})..."
            for peer_id in peer_ids
        ]
        return list(zip(batch, descriptions))
