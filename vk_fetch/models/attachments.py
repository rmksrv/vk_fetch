import dataclasses as dc
import datetime as dt
import typing as t

from vk_fetch import constants, utils
from vk_fetch.models import media_types


AttachmentContent = media_types.Audio | media_types.Photo | dict


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

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            type=constants.MediaType(d.get("type")),
            photo=media_types.Photo.of(d.get("photo")),
            audio=media_types.Audio.of(d.get("audio")),
            **utils.keys_excluded_dict(d, ["photo", "audio", "type"]),
        )

    def content(self) -> AttachmentContent:
        match self.type:
            case constants.MediaType.Photo:
                return self.photo
            case constants.MediaType.Audio:
                return self.audio
            case constants.MediaType.Video:
                return self.video
            case constants.MediaType.Doc:
                return self.doc
            case constants.MediaType.Link:
                return self.link
            case constants.MediaType.Market:
                return self.market
            case constants.MediaType.Wall:
                return self.wall


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
