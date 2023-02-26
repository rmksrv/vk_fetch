import typing as t


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
