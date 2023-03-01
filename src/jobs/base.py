import abc
import typing as t

from src import core, fetchers, utils
from src.logging import log


class VkFetchJob(abc.ABC):
    """
    Base class for vk_fetch jobs
    """

    def __init__(self, api: core.APIProvider):
        self.api = api

    def run(self) -> None:
        """Run job"""


class CheckPermissionsJob(VkFetchJob):
    __slots__ = ("api", "silent")

    def __init__(self, api: core.APIProvider, silent: bool = False):
        super().__init__(api)
        self.silent = silent

    def run(self) -> None:
        permissions = fetchers.granted_permissions(self.api)
        permissions_strs = [
            utils.vk_permission_str(perm) for perm in permissions
        ]
        if not self.silent:
            log(f"Granted permissions: {permissions_strs}")


def run_all(jobs: t.Iterable[VkFetchJob]) -> None:
    for job in jobs:
        job.run()
