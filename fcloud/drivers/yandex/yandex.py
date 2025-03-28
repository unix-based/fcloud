import os
from yadisk import Client
from pathlib import Path
from typing import Callable
from functools import wraps

from yadisk.exceptions import YaDiskConnectionError
from yadisk.exceptions import RequestTimeoutError
from yadisk.exceptions import PathNotFoundError
from yadisk.exceptions import UnauthorizedError
from yadisk.exceptions import ForbiddenError

from .errors import YandexException
from .errors import YandexError
from .models import YandexAuth
from ..base import CloudProtocol
from ...models.settings import CloudObj
from ...utils.other import generate_new_name
from ...exceptions.file_errors import FileError


def yandex_api_error(func: Callable):
    """A decorator that catches errors from the
      Dropbox api and prints them to the user

    Args:
        func (Callable): driver method
    """

    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except YaDiskConnectionError:
            raise YandexException(*YandexError.connection_error)
        except RequestTimeoutError:
            raise YandexException(*YandexError.timed_out_error)
        except PathNotFoundError:
            raise YandexException(*YandexError.path_not_found_error)
        except UnauthorizedError:
            raise YandexException(*YandexError.invalid_token_error)
        except ForbiddenError:
            raise YandexException(*YandexError.access_denied)
        except FileNotFoundError:
            raise YandexException(*FileError.not_exists_error)
        except PermissionError:
            raise YandexException(*FileError.permission_denied)
        except Exception as er:
            title, message = YandexError.unknown_error
            raise YandexException(title.format(er), message.format(er))

    return inner


class YandexCloud(CloudProtocol):
    @yandex_api_error
    def __init__(self, auth: YandexAuth, main_folder: Path):
        self._main_folder = main_folder
        self._auth = auth
        self._app = Client(auth.client_id, auth.client_secret, auth.token)

        if not self._app.check_token():
            raise UnauthorizedError

    @yandex_api_error
    def download_file(self, path: Path, local_path: Path) -> None:
        self._app.download(path.as_posix(), local_path.as_posix())

    @yandex_api_error
    def upload_file(self, local_path: Path, path: Path) -> str:
        filename = os.path.basename(path)
        if not self._app.exists(path.parent.as_posix()):
            raise PathNotFoundError
        files = [file.name for file in self.get_all_files(path.parent)]
        if filename in files:
            filename = generate_new_name(files, filename)
        self._app.upload(
            local_path.as_posix(), path.parent.joinpath(filename).as_posix()
        )

        return filename

    @yandex_api_error
    def get_all_files(self, remote_path: Path) -> list[CloudObj]:
        return [
            CloudObj(
                name=file.name,
                size=file.size,
                is_directory=file.type == "dir",
                modified=file.modified,
            )
            for file in self._app.listdir(remote_path.as_posix())
        ]

    @yandex_api_error
    def remove_file(self, path: Path) -> None:
        self._app.remove(path.as_posix())

    @yandex_api_error
    def info(self, path: Path) -> dict:
        metadata = self._app.get_meta(path.as_posix())
        return {
            "Path": metadata.path,
            "Size": f"{metadata.size} B",
            "Media type": metadata.media_type,
            "Content hash": metadata.md5,
            "Modified": metadata.modified,
            "Antivirus status": metadata.antivirus_status,
        }
