import pathlib
from typing import Optional, Dict, Union

import configargparse
import httpx

from classiq import config

_DEFAULT_CONFIG_FILE_PATH = str(pathlib.Path("classiq", "config.ini"))


class Client:
    def __init__(self):
        arg_parser = configargparse.ArgParser(
            default_config_files=[_DEFAULT_CONFIG_FILE_PATH]
        )

        arg_parser.add_argument(
            "--classiq-config-file",
            is_config_file=True,
            help="Configuration file path",
            env_var="CLASSIQ_CONFIG_FILE",
        )
        arg_parser.add_argument(
            "--classiq-host",
            help="The URL of Classiq's backend host",
            env_var="CLASSIQ_HOST",
        )
        arg_parser.add_argument(
            "--classiq-client-id", help="Your client ID", env_var="CLASSIQ_CLIENT_ID"
        )
        arg_parser.add_argument(
            "--classiq-client-secret",
            help="Your client secret",
            env_var="CLASSIQ_CLIENT_SECRET",
        )

        args, _ = arg_parser.parse_known_args()
        self._config = config.Configuration(
            host=args.classiq_host,
            client_id=args.classiq_client_id,
            client_secret=args.classiq_client_secret,
        )

    async def call_api(
        self, http_method: str, url: str, body: Optional[Dict] = None
    ) -> Union[Dict, str]:
        if not self._config.host:
            raise Exception("Classiq backend host not configured properly.")
        if not self._config.token:
            raise Exception("Access token not generated properly.")

        async with httpx.AsyncClient(base_url=self._config.host) as async_client:
            headers = self._get_authorization_header()
            response = await async_client.request(
                method=http_method, url=url, json=body, headers=headers
            )

        if response.is_error:
            raise Exception(
                f'Call to API failed with code {response.status_code}: {response.json()["detail"]}'
            )

        return response.json()

    def _get_authorization_header(self) -> Dict:
        return {"Authorization": f"Bearer {self._config.token}"}


client = Client()
