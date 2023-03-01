import typing as t

import vk_api as vk

from vk_fetch import constants, core, models
from vk_fetch.models import media_types

UserResponse = list[dict[str, t.Any]]


def granted_permissions(api: core.APIProvider) -> list[vk.VkUserPermissions]:
    response = api.executor.account.getAppPermissions()
    return [
        perm for perm in vk.VkUserPermissions if response | perm == response
    ]


def profile_info(api: core.APIProvider) -> models.ProfileInfo:
    response = api.executor.account.getProfileInfo()
    return models.ProfileInfo.of(response)


def users(
    api: core.APIProvider, user_ids: list[str | int]
) -> list[models.User]:
    user_ids = list(map(str, user_ids))
    response: UserResponse = api.executor.users.get(user_ids=user_ids)
    return [models.User.of(d) for d in response]


def photos(api: core.APIProvider) -> media_types.PhotoList:
    response = api.tools.get_all_iter(
        "photos.getAll", max_count=constants.VK_MAX_ITEMS_COUNT
    )
    return media_types.PhotoList(
        media_types.Photo.of(item) for item in response
    )


def conversations(api: core.APIProvider) -> models.ConversationItemList:
    response = api.tools.get_all_iter(
        "messages.getConversations", max_count=constants.VK_MAX_ITEMS_COUNT
    )
    return models.ConversationItemList(
        models.ConversationItem.of(item) for item in response
    )


def conversation_attachments_iter(
    api: core.APIProvider, peer_id: int, media_type: constants.MediaType
) -> t.Generator[models.AttachmentItem, None, None]:
    response = api.executor.messages.getHistoryAttachments(
        peer_id=peer_id, media_type=media_type.value, max_count=1
    )
    next_from = response.get("next_from")
    items = response.get("items")

    while next_from or items:
        for item in items:
            yield models.AttachmentItem.of(item)

        response = api.executor.messages.getHistoryAttachments(
            peer_id=peer_id,
            media_type=media_type.value,
            max_count=1,
            start_from=next_from,
        )
        next_from = response.get("next_from")
        items = response.get("items")


def _conversations_amount(api: core.APIProvider) -> int:
    return api.executor.messages.getConversations(count=1).get("count")
