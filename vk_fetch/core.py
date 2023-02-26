import vk_api as vk
from loguru import logger

from vk_fetch import constants


class APIProvider:
    DEFAULT_USER_SCOPE = frozenset(
        [
            vk.VkUserPermissions.MESSAGES,
            vk.VkUserPermissions.PHOTOS,
            vk.VkUserPermissions.STATUS,
            vk.VkUserPermissions.VIDEO,
        ]
    )

    @classmethod
    def basic(
        cls,
        login: str,
        password: str,
        scope: set[vk.VkUserPermissions] = DEFAULT_USER_SCOPE,
    ) -> vk.vk_api.VkApiMethod:
        session = vk.VkApi(login, password, scope=sum(scope))
        session.auth()
        logger.info("Successfully authenticated")
        return session.get_api()

    @classmethod
    def kate_mobile(
        cls,
        login: str,
        password: str,
        scope: set[vk.VkUserPermissions] = DEFAULT_USER_SCOPE,
    ) -> vk.vk_api.VkApiMethod:
        session = vk.VkApi(
            login, password, scope=sum(scope), app_id=constants.KATE_MOBILE_APP_ID
        )
        session.auth(token_only=True)
        logger.info("Successfully authenticated")
        return session.get_api()


def permissions_bitmask(
    permissions: list[vk.VkUserPermissions] = vk.VkUserPermissions,
) -> int:
    return sum(permissions)
