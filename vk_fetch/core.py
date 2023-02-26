import typing as t

import vk_api as vk
from loguru import logger

from vk_fetch import constants


class APIProvider:

    __slots__ = ("session", "executor", "tools")

    def __init__(self, session: vk.VkApi):
        self.session = session
        self.executor = session.get_api()
        self.tools = vk.VkTools(session)

    @classmethod
    def basic(
        cls,
        login: str,
        password: str,
        scope: set[vk.VkUserPermissions] = constants.DEFAULT_USER_PERMISSIONS_SCOPE,
    ) -> t.Self:
        session = vk.VkApi(login, password, scope=sum(scope))
        session.auth()
        logger.info("Successfully authenticated")
        return cls(session=session)

    @classmethod
    def kate_mobile(
        cls,
        login: str,
        password: str,
        scope: set[vk.VkUserPermissions] = constants.DEFAULT_USER_PERMISSIONS_SCOPE,
    ) -> t.Self:
        session = vk.VkApi(
            login,
            password,
            scope=sum(scope),
            app_id=constants.KATE_MOBILE_APP_ID,
        )
        session.auth(token_only=True)
        logger.info("Successfully authenticated")
        return cls(session=session)


def permissions_bitmask(
    permissions: list[vk.VkUserPermissions] = vk.VkUserPermissions,
) -> int:
    return sum(permissions)
