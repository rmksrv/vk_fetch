import dataclasses as dc
import datetime as dt
import typing as t

from vk_fetch import constants, utils, models


@dc.dataclass(frozen=True, slots=True)
class Attachment:
    type: constants.MediaType
    photo: models.Photo | None = None
    video: dict | None = None
    audio: dict | None = None
    doc: dict | None = None
    link: dict | None = None
    market: dict | None = None
    wall: dict | None = None

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            photo=models.Photo.of(d.get("photo")),
            **utils.keys_excluded_dict(d, ["photo"])
        )


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
            **utils.keys_excluded_dict(d, ["attachment", "date"])
        )
