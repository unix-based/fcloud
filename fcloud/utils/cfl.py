import os
from pathlib import Path

from ..exceptions.base_errors import FcloudError
from ..exceptions.cfl_errors import CFLError
from ..exceptions.exceptions import FcloudException
from ..exceptions.file_errors import FileError


def create_cfl(
    path: Path, filename: str, main_folder: Path, cfl_extension: str, near: bool = True
) -> None:
    """Create CFL

    Args:
        path (Path): The path for the actual file that was uploaded to the cloud
        filename (str): The name under which the file was saved
        main_folder (Path): The folder in the cloud under which the site was uploaded
        cfl_extension (str): Cfl extension
        near (bool, optional): If True, it will create a cfl near to the main file,
          if False, it will overwrite the file. Defaults to True.
    """
    try:
        new_path = str(path) + cfl_extension
        if not near:
            os.rename(path, new_path)
        with open(new_path, "w", encoding="utf-8") as cfl:
            cfl.write(f"%cfl:{main_folder / filename}")
    except PermissionError:
        raise FcloudException(*FileError.permission_denied)
    except FileExistsError:
        raise FcloudException(*FileError.not_exists_error)
    except Exception as err:
        title, message = FcloudError.unknown_error
        raise FcloudException(title, message.format(err))


def read_cfl(path: Path) -> Path:
    """Read and validate cfl file

    Args:
        path (Path): Path to cfl

    Returns:
        tuple[remote_path, filename]: Returns the default folder path and file name
    """
    if not path.exists():
        raise FcloudException(*CFLError.not_exists_cfl_error)
    with open(path, "r", encoding="utf-8") as cfl:
        data = cfl.readline()
        if is_cfl(data):
            data = data[5:].replace("\n", "")
        else:
            raise FcloudException(*CFLError.incorrect_cfl_error)
    return Path(data)


def is_cfl(cfl: str) -> bool:
    return cfl.startswith("%cfl:")


def delete_cfl(cfl: Path) -> None:
    try:
        os.remove(cfl)
    except PermissionError:
        raise FcloudException(*FileError.permission_denied)
    except FileExistsError:
        raise FcloudException(*FileError.not_exists_error)
    except Exception as err:
        title, message = FcloudError.unknown_error
        raise FcloudException(title, message.format(err))
