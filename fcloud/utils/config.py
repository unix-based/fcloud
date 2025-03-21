import os
import configparser
from typing import Optional

from ..exceptions.config_errors import ConfigError
from ..exceptions.base_errors import FcloudError
from ..exceptions.exceptions import FcloudConfigException


def edit_config(section: str, name: str, value: str) -> None:
    path = os.environ.get("FCLOUD_CONFIG_PATH")  # type: ignore
    config = configparser.ConfigParser()
    config.read(path)
    config[section][name] = value
    try:
        with open(path, "w", encoding="utf-8") as configfile:
            config.write(configfile)
    except FileNotFoundError:
        raise FcloudConfigException(*ConfigError.config_not_found)
    except PermissionError:
        raise FcloudConfigException(*ConfigError.permission_denied)


def get_field(
    parameter: str,
    error: tuple[str, str] = FcloudError.unknown_error,
    config: Optional[configparser.ConfigParser] = None,
    section: str = "FCLOUD",
) -> str:
    if not config:
        path = os.environ.get("FCLOUD_CONFIG_PATH")
        config = configparser.ConfigParser()
        config.read(path)

    try:
        return config[section][parameter]
    except KeyError:
        raise FcloudConfigException(*error)


def get_section(
    section: str = "FCLOUD",
    error: tuple[str, str] = FcloudError.unknown_error,
    config: Optional[configparser.ConfigParser] = None,
) -> configparser.SectionProxy:
    if not config:
        path = os.environ.get("FCLOUD_CONFIG_PATH")
        config = configparser.ConfigParser()
        config.read(path)
    try:
        return config[section.upper()]
    except KeyError:
        raise FcloudConfigException(*error)
