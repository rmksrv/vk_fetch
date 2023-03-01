from src import fetchers
from src.jobs import base
from src.logging import log, kvlog_if_present
from src.utils import yes_or_no


DATETIME_FORMAT = "%Y-%m-%d"


class ShowProfileInfoJob(base.VkFetchJob):
    __slots__ = ("api",)

    def run(self) -> None:
        profile = fetchers.profile_info(self.api)
        log("Profile info fetched")
        kvlog_if_present("ID", profile.id)
        kvlog_if_present("Full name", profile.full_name())
        kvlog_if_present("Screen name", profile.screen_name)
        kvlog_if_present("Birthdate", profile.bdate.strftime(DATETIME_FORMAT))
        kvlog_if_present("Is birthdate visible", profile.bdate_visibility)
        kvlog_if_present("Status", profile.status)
        kvlog_if_present("Sex", profile.sex)
        kvlog_if_present("City", profile.city)
        kvlog_if_present("Country", profile.country)
        kvlog_if_present("Home town", profile.home_town)
        kvlog_if_present("Phone", profile.phone)
        kvlog_if_present("Relation", profile.relation)
        kvlog_if_present(
            "Is Tinkoff linked", yes_or_no(profile.is_tinkoff_linked)
        )
        kvlog_if_present(
            "Is Tinkoff verified", yes_or_no(profile.is_tinkoff_verified)
        )
        kvlog_if_present(
            "Is Sber verified", yes_or_no(profile.is_sber_verified)
        )
        kvlog_if_present("Is Esia linked", yes_or_no(profile.is_esia_linked))
        kvlog_if_present(
            "Is Esia verified", yes_or_no(profile.is_esia_verified)
        )
