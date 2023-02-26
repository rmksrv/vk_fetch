import dataclasses as dc
import typing as t

from vk_fetch import utils


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
class Photo:
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

    @classmethod
    @utils.none_on_throw(AttributeError)
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            sizes=[PhotoSize.of(s) for s in d.get("sizes")],
            **utils.keys_excluded_dict(d, ["sizes"])
        )

    def highest_quality(self) -> PhotoSize:
        return sorted(self.sizes, key=lambda s: s.width)[-1]
