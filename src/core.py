import concurrent.futures
import dataclasses as dc
import datetime as dt
import http
import os
import pathlib
import typing as t

import requests
import vk_api as vk
from requests import ConnectTimeout
from urllib3.exceptions import ConnectTimeoutError

from src import constants, utils
from src.logging import log


class APIProvider:
    __slots__ = ("session", "executor", "tools")

    def __init__(self, session: vk.VkApi):
        self.session = session
        self.executor = session.get_api()
        self.tools = vk.VkTools(session)

    @classmethod
    def basic(
        cls,
        login: str,
        password: str,
        scope: set[
            vk.VkUserPermissions
        ] = constants.DEFAULT_USER_PERMISSIONS_SCOPE,
    ) -> t.Self:
        session = vk.VkApi(login, password, scope=permissions_bitmask(scope))
        session.auth()
        log("  Successfully authenticated ✅ .")
        return cls(session=session)

    @classmethod
    def kate_mobile(
        cls,
        login: str,
        password: str,
        scope: set[
            vk.VkUserPermissions
        ] = constants.DEFAULT_USER_PERMISSIONS_SCOPE,
    ) -> t.Self:
        session = vk.VkApi(
            login,
            password,
            scope=permissions_bitmask(scope),
            app_id=constants.KATE_MOBILE_APP_ID,
        )
        session.auth(token_only=True)
        log("  Successfully authenticated ✅ .")
        return cls(session=session)


def permissions_bitmask(
    permissions: t.Iterable[vk.VkUserPermissions] = vk.VkUserPermissions,
) -> int:
    return sum(permissions)


@dc.dataclass(frozen=True, slots=True)
class DownloadItem:
    url: str
    destination: pathlib.Path
    modification_time: dt.datetime = dt.datetime.now()

    @utils.return_on_throw(
        constants.DownloadStatus.Failed, ConnectTimeoutError, ConnectTimeout
    )
    def download(self) -> constants.DownloadStatus:
        download_file_path = (
            self.destination.resolve() / utils.crop_url_to_filename(self.url)
        )
        resp = requests.get(self.url, stream=True)
        match resp.status_code:
            case http.HTTPStatus.OK:
                download_file_path.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with download_file_path.open("wb") as buf:
                        for chunk in resp:
                            buf.write(chunk)
                    self.set_new_modtime_to_downloaded_file(download_file_path)
                    return constants.DownloadStatus.Success
                except Exception:
                    return constants.DownloadStatus.Failed
            case _:
                return constants.DownloadStatus.Failed

    def set_new_modtime_to_downloaded_file(self, file_path: pathlib.Path):
        dt_epoch = self.modification_time.timestamp()
        os.utime(str(file_path), (dt_epoch, dt_epoch))


@dc.dataclass(slots=True)
class DownloadResult:
    succeed: list[DownloadItem] = dc.field(default_factory=list)
    failed: list[DownloadItem] = dc.field(default_factory=list)


def download_files_parallel(
    items: t.Iterable[DownloadItem], max_workers: int = 5
) -> DownloadResult:
    result = DownloadResult()
    with concurrent.futures.ThreadPoolExecutor(
        max_workers=max_workers
    ) as executor:
        future_to_download_result = {
            executor.submit(item.download): item for item in items
        }
        for future in concurrent.futures.as_completed(
            future_to_download_result
        ):
            item = future_to_download_result[future]
            match future.result():
                case constants.DownloadStatus.Success:
                    result.succeed.append(item)
                case constants.DownloadStatus.Failed:
                    result.failed.append(item)
    return result
