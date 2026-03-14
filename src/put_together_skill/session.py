from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Session:
    access_token: str
    refresh_token: str
    expires_at: str | None
    linked_user: dict[str, Any] | None
    agent: dict[str, Any] | None

    @classmethod
    def from_response(cls, payload: dict[str, Any]) -> "Session":
        expires_in = payload.get("expires_in")
        expires_at = None
        if isinstance(expires_in, int):
            expires_at = (utc_now() + timedelta(seconds=expires_in)).isoformat()

        return cls(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_at=expires_at,
            linked_user=payload.get("linked_user"),
            agent=payload.get("agent"),
        )

    @classmethod
    def load(cls, path: Path) -> "Session | None":
        if not path.exists():
            return None
        payload = json.loads(path.read_text(encoding="utf-8"))
        return cls(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_at=payload.get("expires_at"),
            linked_user=payload.get("linked_user"),
            agent=payload.get("agent"),
        )

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "access_token": self.access_token,
                    "refresh_token": self.refresh_token,
                    "expires_at": self.expires_at,
                    "linked_user": self.linked_user,
                    "agent": self.agent,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )

    def is_expired(self) -> bool:
        if not self.expires_at:
            return False
        try:
            return datetime.fromisoformat(self.expires_at) <= utc_now()
        except ValueError:
            return False
