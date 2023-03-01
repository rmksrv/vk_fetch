import dataclasses as dc
import typing as t
import functools

import vk_api.vk_api

from vk_fetch import constants


def keys_excluded_dict(d: dict, keys: t.Iterable) -> dict:
    return {x: d[x] for x in d if x not in keys}


def none_on_throw(*exs: type[BaseException]):
    OfFactoryMethod = t.Callable[[...], t.Any]

    def _decorator(func: OfFactoryMethod):
        def _wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except exs:
                res = None
            return res

        return _wrapper

    return _decorator


def peer_id_from_sel(sel: str) -> int:
    if sel.startswith("c"):
        return constants.VK_GROUP_PEER_ID_SINCE + int(sel[1:])
    return int(sel)


def yes_or_no(v: bool) -> str:
    return "yes" if v else "no"


def crop_url_to_filename(url: str) -> str:
    no_root = url.split("/")[-1]
    return no_root.split("?")[0]


def vk_permission_str(p: vk_api.vk_api.VkUserPermissions) -> str:
    return p.name


@dc.dataclass(slots=True)
class AttachmentsCounter:
    uniques: int = 0
    duplicates: int = 0

    @classmethod
    def sum(cls, _it: t.Iterable["AttachmentsCounter"]) -> t.Self:
        return functools.reduce(cls.__add__, _it)

    def __add__(self, other: t.Self) -> t.Self:
        return AttachmentsCounter(
            uniques=self.uniques + other.uniques,
            duplicates=self.duplicates + other.duplicates,
        )
