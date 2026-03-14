from __future__ import annotations

import json
import urllib.error
import urllib.request
from typing import Any

from put_together_skill.config import Config
from put_together_skill.session import Session


class BridgeError(RuntimeError):
    pass


class BridgeClient:
    def __init__(self, config: Config) -> None:
        self.config = config

    def _request(
        self,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
        access_token: str | None = None,
    ) -> dict[str, Any]:
        data = None
        headers = {"Accept": "application/json"}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"
        if access_token:
            headers["Authorization"] = f"Bearer {access_token}"

        request = urllib.request.Request(
            f"{self.config.bridge_url}{path}",
            data=data,
            headers=headers,
            method=method,
        )

        try:
            with urllib.request.urlopen(request, timeout=self.config.timeout_seconds) as response:
                body = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise BridgeError(f"{method} {path} failed with {exc.code}: {body}") from exc
        except urllib.error.URLError as exc:
            raise BridgeError(f"{method} {path} failed: {exc.reason}") from exc

        if not body:
            return {}

        try:
            return json.loads(body)
        except json.JSONDecodeError as exc:
            raise BridgeError(f"{method} {path} returned non-JSON response") from exc

    def link_exchange(self, code: str) -> Session:
        payload = {
            "code": code,
            "agent": {
                "id": self.config.agent_id,
                "name": self.config.agent_name,
                "platform": "openclaw",
            },
        }
        response = self._request("POST", "/v1/link/exchange", payload=payload)
        return Session.from_response(response)

    def refresh_session(self, refresh_token: str) -> Session:
        response = self._request(
            "POST",
            "/v1/session/refresh",
            payload={"refresh_token": refresh_token},
        )
        return Session.from_response(response)

    def session_status(self, access_token: str) -> dict[str, Any]:
        return self._request("GET", "/v1/session", access_token=access_token)

    def recommendation(self, path: str, payload: dict[str, Any], access_token: str) -> dict[str, Any]:
        return self._request("POST", path, payload=payload, access_token=access_token)
