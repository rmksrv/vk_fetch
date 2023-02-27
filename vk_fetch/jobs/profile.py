from loguru import logger

from vk_fetch import fetchers
from vk_fetch.jobs import base
from vk_fetch.utils import (
    log_if_present as log,
    yes_or_no,
)


DATETIME_FORMAT = "%Y-%m-%d"


class ShowProfileJob(base.VkFetchJob):
    def run(self) -> None:
        profile = fetchers.profile_info(self.api)
        logger.info("Profile info fetched")
        log("ID", profile.id)
        log("Full name", profile.full_name())
        log("Screen name", profile.screen_name)
        log("Birthdate", profile.bdate.strftime(DATETIME_FORMAT))
        log("Is birthdate visible", profile.bdate_visibility)
        log("Status", profile.status)
        log("Sex", profile.sex)
        log("City", profile.city)
        log("Country", profile.country)
        log("Home town", profile.home_town)
        log("Phone", profile.phone)
        log("Relation", profile.relation)
        log("Is Tinkoff linked", yes_or_no(profile.is_tinkoff_linked))
        log("Is Tinkoff verified", yes_or_no(profile.is_tinkoff_verified))
        log("Is Sber verified", yes_or_no(profile.is_sber_verified))
        log("Is Esia linked", yes_or_no(profile.is_esia_linked))
        log("Is Esia verified", yes_or_no(profile.is_esia_verified))
