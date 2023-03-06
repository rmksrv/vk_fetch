import collections
import dataclasses as dc
import datetime as dt
import pathlib
import typing as t

from vk_fetch import utils, core
from vk_fetch.models.media_types import media


@dc.dataclass(frozen=True, slots=True)
class PhotoSize:
    type: str
    width: int
    height: int
    url: str

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(**d)


@dc.dataclass(frozen=True, slots=True)
class Photo(media.Media):
    id: int
    date: int
    album_id: int
    owner_id: int
    sizes: list[PhotoSize]
    text: str
    user_id: int | None = None
    access_key: str | None = None
    post_id: int | None = None
    square_crop: str | None = None
    lat: float | None = None
    long: float | None = None

    def __str__(self):
        return f"Photo {self.highest_quality().url}"

    def __hash__(self):
        return self.id

    @classmethod
    @utils.none_on_throw(AttributeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            sizes=[PhotoSize.of(s) for s in d.get("sizes")],
            **utils.keys_excluded_dict(d, ["sizes"]),
        )

    def highest_quality(self) -> PhotoSize:
        return sorted(self.sizes, key=lambda s: s.width)[-1]

    def download_item(
        self,
        destination: pathlib.Path,
        modification_time: dt.datetime = dt.datetime.now(),
    ) -> core.DownloadItem:
        return core.DownloadItem(
            url=self.highest_quality().url,
            destination=destination,
            modification_time=modification_time,
        )


class PhotoList(collections.UserList):
    def highest_quality_urls(self) -> list[str]:
        return [photo.highest_quality().url for photo in self]

    def download_items(
        self, destination: pathlib.Path
    ) -> list[core.DownloadItem]:
        return [photo.download_item(destination) for photo in self]
