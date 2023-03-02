import dataclasses as dc
import datetime as dt
import pathlib
import typing as t

from src import utils, core
from src.models.media_types import media


@dc.dataclass(frozen=True, slots=True)
class AudioAds:
    content_id: str
    duration: str
    account_age_type: str
    puid1: str
    puid22: str

    @classmethod
    @utils.none_on_throw(TypeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(**d)


@dc.dataclass(frozen=True, slots=True)
class Audio(media.Media):
    id: int
    artist: str
    owner_id: int
    title: str
    duration: dt.timedelta
    date: dt.datetime
    is_explicit: bool
    is_licensed: bool
    url: str
    short_videos_allowed: bool
    stories_allowed: bool
    stories_cover_allowed: bool
    ads: AudioAds
    access_key: str | None = None
    subtitle: str | None = None
    content_restricted: int | None = None
    genre_id: int | None = None
    album_id: int | None = None
    lyrics_id: int | None = None
    no_search: int | None = None
    main_artists: list[dict] | None = None
    featured_artists: list[dict] | None = None

    @classmethod
    @utils.none_on_throw(AttributeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        exclude_fields = ["date", "duration", "ads"]
        return cls(
            date=dt.datetime.fromtimestamp(int(d.get("date"))),
            duration=dt.timedelta(seconds=int(d.get("duration"))),
            ads=AudioAds.of(d.get("ads")),
            **utils.keys_excluded_dict(d, exclude_fields),
        )

    def download_item(
        self, destination: pathlib.Path, modification_time: dt.datetime
    ) -> core.DownloadItem:
        raise NotImplemented

    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f'Audio "{self.artist} - {self.title} ({self.duration})"'
