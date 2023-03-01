import pathlib

from src import fetchers, core, constants
from src.jobs import base
from src.models import media_types
from src.logging import log, kvlog_if_present


class ShowPhotosJob(base.VkFetchJob):
    __slots__ = ("api",)

    def run(self) -> None:
        photos = fetchers.photos(self.api)
        log("Photos fetched")
        for photo in photos:
            log_photo(photo)


def log_photo(photo: media_types.Photo) -> None:
    log(f"  Photo(ID={photo.id})")
    kvlog_if_present("Date", photo.date)
    kvlog_if_present("Album ID", photo.album_id)
    kvlog_if_present("Owner ID", photo.owner_id)
    kvlog_if_present("Highest res URL", photo.highest_quality().url)
    kvlog_if_present("Text", photo.text)


class DownloadPhotosJob(base.VkFetchJob):
    __slots__ = ("api", "destination")

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
            log("Some of photos were not downloaded:")
            for item in download_results.failed:
                log(f" - {item.url}")
        log(f"  Downloaded photos: {len(download_results.succeed)}")
