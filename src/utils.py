import dataclasses as dc
import functools
import re
import typing as t

from vk_api import vk_api

from src import constants


def keys_excluded_dict(d: dict, keys: t.Iterable) -> dict:
    return {x: d[x] for x in d if x not in keys}


def return_on_throw(retval, *exs: type[BaseException]):
    def _decorator(func: t.Callable):
        def _wrapper(*args, **kwargs):
            try:
                res = func(*args, **kwargs)
            except exs:
                res = retval
            return res

        return _wrapper

    return _decorator


def none_on_throw(*exs: type[BaseException]):
    return return_on_throw(None, *exs)


OfFactoryMethod = t.Callable[[t.Type, dict[str, t.Any]], t.Any]


def none_on_empty_dict(of_func: OfFactoryMethod):
    def _wrapper(cls: t.Type, d: dict[str, t.Any]):
        return None if d is None else of_func(cls, d)

    return _wrapper


def peer_id_from_sel(sel: str) -> int:
    if sel.startswith("c"):
        return constants.VK_GROUP_PEER_ID_SINCE + int(sel[1:])
    return int(sel)


def yes_or_no(v: bool) -> str:
    return "yes" if v else "no"


def crop_url_to_filename(url: str) -> str:
    no_root = url.split("/")[-1]
    return no_root.split("?")[0]


def vk_permission_str(p: vk_api.VkUserPermissions) -> str:
    return p.name


@dc.dataclass(slots=True)
class AttachmentsCounter:
    uniques: int = 0
    duplicates: int = 0
    succeed: int = 0
    failed: int = 0

    @classmethod
    def sum(cls, _it: t.Iterable["AttachmentsCounter"]) -> t.Self:
        return functools.reduce(cls.__add__, _it)

    def __add__(self, other: t.Self) -> t.Self:
        return AttachmentsCounter(
            uniques=self.uniques + other.uniques,
            duplicates=self.duplicates + other.duplicates,
            succeed=self.succeed + other.succeed,
            failed=self.failed + other.failed,
        )


def sanitize_fspath(path: str):
    return re.sub(r"[^\w_. -]", "_", path)
