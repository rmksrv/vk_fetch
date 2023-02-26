import typing as t


def keys_excluded_dict(d: dict, keys: t.Iterable) -> dict:
    return {x: d[x] for x in d if x not in keys}
