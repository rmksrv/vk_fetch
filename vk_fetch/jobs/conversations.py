import pathlib
import typing as t

from vk_fetch import core, constants, fetchers, models, utils
from vk_fetch.jobs import base
from vk_fetch.logging import log


class ShowConversationAttachmentsJob(base.VkFetchJob):
    __slots__ = (
        "api",
        "peer_id",
        "user",
        "media_types",
    )

    def __init__(
        self,
        api: core.APIProvider,
        peer_id: int | None = None,
        user: models.User | None = None,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ):
        assert bool(peer_id) ^ bool(
            user
        ), 'Neither "peer_id" nor "user" was provided or was provided both'
        super().__init__(api)
        self.user = user or fetchers.users(api, [peer_id])
        self.peer_id = peer_id or self.user.id
        self.media_types = media_types

    def run(self) -> None:
        counters: dict[constants.MediaType, utils.AttachmentsCounter] = {
            mt: utils.AttachmentsCounter() for mt in self.media_types
        }
        for media_type in self.media_types:
            attachment_hashes = set()
            for attachment_item in fetchers.conversation_attachments_iter(
                self.api, self.peer_id, media_type
            ):
                attachment_content = attachment_item.attachment.content()
                attachment_hash = hash(attachment_content)
                if attachment_hash in attachment_hashes:
                    counters[media_type].duplicates += 1
                    continue
                log(
                    f"  Attachment {attachment_content} from message at {attachment_item.date}"
                )
                attachment_hashes.add(attachment_hash)
                counters[media_type].uniques += 1
        for media_type in self.media_types:
            log(
                f"  {media_type.name}: {counters[media_type].uniques} items "
                f"({counters[media_type].duplicates} duplicates)"
            )
        total = utils.AttachmentsCounter.sum(counters.values())
        log(
            f"  Total: {total.uniques} ({total.duplicates} duplicates) items "
            f"from {self.user.full_name()} conversation"
        )

    @classmethod
    def batch(
        cls,
        api: core.APIProvider,
        peer_ids: list[int] | None = None,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ) -> list[t.Self]:
        users = fetchers.users(api, peer_ids)
        return [
            cls(
                api,
                user=user,
                media_types=media_types,
            )
            for user in users
        ]

    @classmethod
    def batch_with_description(
        cls,
        api: core.APIProvider,
        peer_ids: list[int | str],
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ) -> list[tuple[t.Self, str]]:
        batch = cls.batch(
            api,
            peer_ids=peer_ids,
            media_types=media_types,
        )
        descriptions = [
            f"Fetching attachments of {job.user.full_name()} conversation..."
            for job in batch
        ]
        return list(zip(batch, descriptions))


class DownloadConversationAttachmentsJob(base.VkFetchJob):
    __slots__ = (
        "api",
        "conversation_item",
        "destination",
        "media_types",
        "max_files_in_batch",
    )

    def __init__(
        self,
        api: core.APIProvider,
        conversation_item: models.ConversationItem,
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
        max_files_in_batch: int = 10,
    ):
        super().__init__(api)
        self.conversation_item = conversation_item
        self.destination = destination
        self.media_types = media_types
        self.max_files_in_batch = max_files_in_batch
        self.peer_name = self.conversation_item.peer_info(self.api).full_name()

    def run(self) -> None:
        counters: dict[constants.MediaType, utils.AttachmentsCounter] = {
            mt: utils.AttachmentsCounter() for mt in self.media_types
        }
        for media_type in self.media_types:
            attachment_hashes = set()
            download_batch = []
            for attachment_item in fetchers.conversation_attachments_iter(
                self.api,
                self.conversation_item.conversation.peer.id,
                media_type,
            ):
                attachment_content = attachment_item.attachment.content()
                attachment_hash = hash(attachment_content)
                if attachment_hash in attachment_hashes:
                    counters[media_type].duplicates += 1
                    continue
                attachment_hashes.add(attachment_hash)
                counters[media_type].uniques += 1

                download_batch.append(
                    attachment_content.download_item(self.destination)
                )
                if len(download_batch) == self.max_files_in_batch:
                    core.download_files_parallel(download_batch)
                    download_batch.clear()

        for media_type in self.media_types:
            log(
                f"  {media_type.name}: {counters[media_type].uniques} items "
                f"({counters[media_type].duplicates} duplicates)"
            )
        total = utils.AttachmentsCounter.sum(counters.values())
        log(
            f"  Total: {total.uniques} ({total.duplicates} duplicates) items "
            f"from {self.peer_name} conversation"
        )

    @classmethod
    def batch(
        cls,
        api: core.APIProvider,
        conversations_items: models.ConversationItemList,
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ) -> list[t.Self]:
        return [
            cls(
                api,
                conversation_item=item,
                destination=destination,
                media_types=media_types,
            )
            for item in conversations_items
        ]

    @classmethod
    def batch_with_description(
        cls,
        api: core.APIProvider,
        conversation_items: models.ConversationItemList,
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
        media_types: t.Iterable[
            constants.MediaType
        ] = constants.DEFAULT_CONVERSATION_MEDIA_TYPES,
    ) -> list[tuple[t.Self, str]]:
        batch = cls.batch(
            api,
            conversations_items=conversation_items,
            destination=destination,
            media_types=media_types,
        )
        descriptions = [
            f"Downloading attachments of {job.peer_name} conversation..."
            for job in batch
        ]
        return list(zip(batch, descriptions))
