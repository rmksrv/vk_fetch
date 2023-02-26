import typing as t

from vk_fetch import constants


def keys_excluded_dict(d: dict, keys: t.Iterable) -> dict:
    return {x: d[x] for x in d if x not in keys}


OfFactoryMethod = t.Callable[[...], t.Any]


def none_on_throw(*exs: type[BaseException]):
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
