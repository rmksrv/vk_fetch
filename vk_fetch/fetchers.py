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


def conversations(api: core.APIProvider):
    response = api.tools.get_all(
        "messages.getConversations", max_count=constants.VK_MAX_ITEMS_COUNT
    )
    return [models.ConversationItem.of(item) for item in response.get("items")]


def conversation_attachments(
    api: core.APIProvider, peer_id: int, media_type: constants.MediaType
) -> list[models.AttachmentItem]:
    response = api.executor.messages.getHistoryAttachments(
        peer_id=peer_id, media_type=media_type.value
    )
    return [models.AttachmentItem.of(item) for item in response.get("items")]


def _conversations_amount(api: core.APIProvider) -> int:
    return api.executor.messages.getConversations(count=1).get("count")
