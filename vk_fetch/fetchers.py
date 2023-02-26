import vk_api as vk

from vk_fetch import models


def profile_info(api: vk.vk_api.VkApiMethod) -> models.ProfileInfo:
    response = api.account.getProfileInfo()
    return models.ProfileInfo.of(response)


def photos(api: vk.vk_api.VkApiMethod) -> list[models.PhotoSize]:
    response = api.photos.getAll()
    return [models.Photo.of(item).highest_quality for item in response.get("items")]
