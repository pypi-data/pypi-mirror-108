import http.client
import json
from typing import Optional

import pydantic

TOKEN = "token"
HOST = "host"

_AUTH0_URL = "classiq.eu.auth0.com"
_AUTH0_AUDIENCE = "https://cadmium-be"


class Configuration(pydantic.BaseModel):
    host: Optional[pydantic.AnyUrl] = None
    client_id: Optional[str] = None
    client_secret: Optional[str] = None

    _token: Optional[str] = pydantic.PrivateAttr(default=None)

    @property
    def token(self) -> str:
        if self._token:
            return self._token

        if not (self.client_id and self.client_secret):
            raise Exception(
                "Token cannot be generated without client ID and client secret."
            )

        self._generate_token()
        return self._token

    def _generate_token(self) -> None:
        if self._token:
            return

        conn = http.client.HTTPSConnection(_AUTH0_URL)
        payload_dict = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "audience": _AUTH0_AUDIENCE,
            "grant_type": "client_credentials",
        }
        payload = json.dumps(payload_dict)
        headers = {"content-type": "application/json"}
        conn.request("POST", "/oauth/token", payload, headers)

        # TODO: check response is legal
        res = conn.getresponse()
        data = json.loads(res.read().decode("utf-8"))
        self._token = data["access_token"]
