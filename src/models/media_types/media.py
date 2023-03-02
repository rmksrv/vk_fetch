import abc
import datetime as dt
import pathlib

from src import core


class Media(abc.ABC):
    @abc.abstractmethod
    def download_item(
        self, destination: pathlib.Path, modification_time: dt.datetime
    ) -> core.DownloadItem:
        """Creates DownloadItem object"""

    @abc.abstractmethod
    def __hash__(self):
        ...
