import dataclasses as dc
import typing as t

from src import models, utils


@dc.dataclass(frozen=True, slots=True)
class Message:
    id: int
    date: int
    peer_id: int
    from_id: int
    conversation_message_id: int
    out: int
    important: bool
    text: str
    is_hidden: bool
    random_id: int
    attachments: list[models.Attachment]
    fwd_messages: list[t.Self]
    ref: str | None = None

    @classmethod
    @utils.none_on_empty_dict
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            attachments=[
                models.Attachment.of(att) for att in d.get("attachments")
            ],
            fwd_messages=[],
            **utils.keys_excluded_dict(
                d, ["attachments", "fwd_messages", "action"]
            )
        )
