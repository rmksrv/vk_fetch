import dataclasses as dc
import datetime as dt
import typing as t

import dateutil.parser

from vk_fetch import utils, constants


@dc.dataclass(frozen=True, slots=True)
class ProfileInfo:
    id: int
    home_town: str
    status: str
    is_tinkoff_linked: bool
    is_tinkoff_verified: bool
    is_sber_verified: bool
    first_name: str
    last_name: str
    bdate: dt.datetime
    bdate_visibility: bool
    city: str
    country: str
    phone: str
    relation: constants.Relation
    sex: constants.Sex

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            bdate=dateutil.parser.parse(d.get("bdate")),
            relation=constants.Relation(d.get("relation")),
            sex=constants.Sex(d.get("sex")),
            city=d.get("city").get("title"),
            country=d.get("country").get("title"),
            **utils.keys_excluded_dict(
                d, ["bdate", "relation", "sex", "city", "country"]
            )
        )


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
    post_id: int
    sizes: list[PhotoSize]
    square_crop: str
    text: str

    @classmethod
    def of(cls, d: dict[str, t.Any]) -> t.Self:
        return cls(
            sizes=[PhotoSize.of(s) for s in d.get("sizes")],
            **utils.keys_excluded_dict(d, ["sizes"])
        )

    @property
    def highest_quality(self) -> PhotoSize:
        return sorted(self.sizes, key=lambda s: s.width)[-1]
