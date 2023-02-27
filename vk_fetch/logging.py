import typing as t

import rich
from loguru import logger

from vk_fetch import constants


def configure_logger() -> None:
    logger.remove(0)
    logger.add(constants.LOGS_PATH / "file_{time}.log")


def log(s: t.Any, level: str = "INFO") -> None:
    ls = s.rstrip() if isinstance(s, str) else s
    logger.log(level, ls)
    rich.print(s)


def kvlog_if_present(k: str, v: t.Any | None) -> None:
    if v:
        log(f"  {k + ':':<25} {v}")
