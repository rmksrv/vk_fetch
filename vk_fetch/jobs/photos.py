import pathlib

from loguru import logger

from vk_fetch import fetchers, models, core, constants
from vk_fetch.jobs import base
from vk_fetch.utils import log_if_present as log


class ShowPhotosJob(base.VkFetchJob):
    def run(self) -> None:
        photos = fetchers.photos(self.api)
        for photo in photos:
            ShowPhotosJob.log_photo(photo)

    @staticmethod
    def log_photo(photo: models.Photo) -> None:
        logger.info(f"Photo(ID={photo.id})")
        log("Date", photo.date)
        log("Album ID", photo.album_id)
        log("Owner ID", photo.owner_id)
        log("Highest res URL", photo.highest_quality().url)
        log("Text", photo.text)


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
