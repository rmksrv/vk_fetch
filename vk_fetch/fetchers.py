import typing as t

import vk_api as vk

from vk_fetch import models, constants, core


def granted_permissions(api: core.APIProvider) -> list[vk.VkUserPermissions]:
    response = api.executor.account.getAppPermissions()
    return [
        perm for perm in vk.VkUserPermissions if response | perm == response
    ]


def profile_info(api: core.APIProvider) -> models.ProfileInfo:
    response = api.executor.account.getProfileInfo()
    return models.ProfileInfo.of(response)


def photos(api: core.APIProvider) -> list[models.PhotoSize]:
    response = api.tools.get_all(
        "photos.getAll", max_count=constants.VK_MAX_ITEMS_COUNT
    )
    return [
        models.Photo.of(item).highest_quality()
        for item in response.get("items")
    ]


def conversations(api: core.APIProvider) -> models.ConversationItemList:
    response = api.tools.get_all(
        "messages.getConversations", max_count=constants.VK_MAX_ITEMS_COUNT
    )
    return models.ConversationItemList(
        models.ConversationItem.of(item) for item in response.get("items")
    )


def conversation_attachments_iter(
    api: core.APIProvider, peer_id: int, media_type: constants.MediaType
) -> t.Generator[models.AttachmentItem, None, None]:
    response = api.tools.get_all_iter(
        "messages.getHistoryAttachments",
        100,
        {"peer_id": peer_id, "media_type": media_type.value},
    )
    for item in response:
        yield models.AttachmentItem.of(item)


def _conversations_amount(api: core.APIProvider) -> int:
    return api.executor.messages.getConversations(count=1).get("count")
