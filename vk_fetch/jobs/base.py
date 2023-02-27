import abc
import typing as t

from vk_fetch import core, fetchers
from vk_fetch.logging import log


class VkFetchJob(abc.ABC):
    """
    Base class for vk_fetch jobs
    """

    def __init__(self, api: core.APIProvider):
        self.api = api

    def run(self) -> None:
        """Run job"""


class CheckPermissionsJob(VkFetchJob):
    def __init__(self, api: core.APIProvider, silent: bool = False):
        super().__init__(api)
        self.silent = silent

    def run(self) -> None:
        permissions = fetchers.granted_permissions(self.api)
        if not self.silent:
            log("Granted permissions:")
            log(permissions)


def run_all(jobs: t.Iterable[VkFetchJob]) -> None:
    for job in jobs:
        job.run()
