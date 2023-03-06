import dataclasses as dc
import typing as t

from vk_fetch import models, utils


@dc.dataclass(frozen=True, slots=True)
class Message:
    id: int
    date: int
    peer_id: int
    from_id: int
    conversation_message_id: int
    text: str
    attachments: list[models.Attachment]
    fwd_messages: list[t.Self]
    payload: dict | None = None
    is_hidden: bool | None = None
    out: int | None = None
    random_id: int | None = None
    important: bool | None = None
    ref: str | None = None

    @classmethod
    @utils.none_on_empty_dict
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        exclude_fileds = [
            "attachments",
            "fwd_messages",
            "action",
            "message_tag",
            "keyboard",
            "geo",
        ]
        return cls(
            attachments=[
                models.Attachment.of(att) for att in d.get("attachments")
            ],
            fwd_messages=[],
            **utils.keys_excluded_dict(d, exclude_fileds)
        )
