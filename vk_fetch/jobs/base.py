import abc
import typing as t

from loguru import logger

from vk_fetch import core, fetchers


class VkFetchJob(abc.ABC):
    """
    Base class for vk_fetch jobs
    """

    def __init__(self, api: core.APIProvider):
        self.api = api

    def run(self) -> None:
        """Run job"""


class CheckPermissionsJob(VkFetchJob):
    def run(self) -> None:
        permissions = fetchers.granted_permissions(self.api)
        logger.info("Granted permissions:")
        logger.info(permissions)


def run_all(jobs: t.Iterable[VkFetchJob]) -> None:
    for job in jobs:
        job.run()
