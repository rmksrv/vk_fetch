import dataclasses as dc
import datetime as dt
import pathlib
import typing as t

from src import constants, utils, core
from src.models import media_types


@dc.dataclass(frozen=True, slots=True)
class Attachment:
    type: constants.MediaType
    photo: media_types.Photo | None = None
    video: dict | None = None
    audio: media_types.Audio | None = None
    doc: dict | None = None
    link: dict | None = None
    market: dict | None = None
    wall: dict | None = None
    poll: dict | None = None
    gift: dict | None = None
    sticker: dict | None = None

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            type=constants.MediaType(d.get("type")),
            photo=media_types.Photo.of(d.get("photo")),
            audio=media_types.Audio.of(d.get("audio")),
            **utils.keys_excluded_dict(d, ["photo", "audio", "type"]),
        )

    def content(self) -> media_types.Media:
        match self.type:
            case constants.MediaType.Photo:
                return self.photo
            case constants.MediaType.Audio:
                return self.audio
            case _:
                raise NotImplementedError


@dc.dataclass(frozen=True, slots=True)
class AttachmentItem:
    message_id: int
    date: dt.datetime
    from_id: int
    cmid: int
    attachment: Attachment
    forward_level: int | None = None

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            attachment=Attachment.of(d.get("attachment")),
            date=dt.datetime.fromtimestamp(int(d.get("date"))),
            **utils.keys_excluded_dict(d, ["attachment", "date"]),
        )

    def download_item(self, destination: pathlib.Path) -> core.DownloadItem:
        return self.attachment.content().download_item(destination)
