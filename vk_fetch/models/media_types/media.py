import abc
import pathlib

from vk_fetch import core


class Media(abc.ABC):
    @abc.abstractmethod
    def download_item(self, destination: pathlib.Path) -> core.DownloadItem:
        """Creates DownloadItem object"""

    @abc.abstractmethod
    def __hash__(self):
        ...
