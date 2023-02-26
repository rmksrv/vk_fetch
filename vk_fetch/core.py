import vk_api as vk
from loguru import logger


@logger.catch
def new_api(login: str, password: str, token: str) -> vk.vk_api.VkApiMethod:
    session = vk.VkApi(login=login, password=password, token=token)
    session.auth()
    logger.info("Successfully authenticated")
    return session.get_api()
