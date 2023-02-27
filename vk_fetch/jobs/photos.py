import pathlib

from vk_fetch import fetchers, models, core, constants
from vk_fetch.jobs import base
from vk_fetch.logging import log, kvlog_if_present


class ShowPhotosJob(base.VkFetchJob):
    def run(self) -> None:
        photos = fetchers.photos(self.api)
        for photo in photos:
            ShowPhotosJob.log_photo(photo)

    @staticmethod
    def log_photo(photo: models.Photo) -> None:
        log(f"Photo(ID={photo.id})")
        kvlog_if_present("Date", photo.date)
        kvlog_if_present("Album ID", photo.album_id)
        kvlog_if_present("Owner ID", photo.owner_id)
        kvlog_if_present("Highest res URL", photo.highest_quality().url)
        kvlog_if_present("Text", photo.text)


class DownloadPhotosJob(base.VkFetchJob):
    def __init__(
        self,
        api: core.APIProvider,
        destination: pathlib.Path = constants.DEFAULT_DESTINATION_PATH,
    ):
        super().__init__(api)
        self.destination = destination

    def run(self) -> None:
        photos = fetchers.photos(self.api)
        download_results = core.download_files_parallel(
            photos.download_items(self.destination)
        )
        if download_results.failed:
            pass
