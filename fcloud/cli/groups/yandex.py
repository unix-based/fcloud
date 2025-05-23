import os
import yadisk

from ...exceptions.config_errors import ConfigError
from ...utils.config import edit_config
from ...utils.config import get_field


class Yandex:
    def __init__(self):
        self._conf = os.environ["FCLOUD_CONFIG_PATH"]
        title, message = ConfigError.field_error
        error = (title, message.format("client_id", self._conf))
        self._client_id = get_field("client_id", error, section="YANDEX")

        error = (title, message.format("client_secret", self._conf))
        self._client_secret = get_field("client_secret", error, section="YANDEX")

        self._app = yadisk.Client(self._client_id, self._client_secret)

    def get_token(self):
        """Generates a code that must be validated by clicking
        on the link to receive the token"""
        url = self._app.get_code_url()
        print(f"Go to the following url: {url}")
        code = input("Enter the confirmation code: ")

        response = self._app.get_token(code)
        edit_config("YANDEX", "token", response.access_token)
