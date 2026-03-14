from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _default_state_dir() -> Path:
    openclaw_state = os.getenv("OPENCLAW_STATE_DIR")
    if openclaw_state:
        return Path(openclaw_state)
    return Path.home() / ".openclaw" / "state"


def default_session_path() -> Path:
    override = os.getenv("PUT_TOGETHER_SESSION_PATH")
    if override:
        return Path(override).expanduser()
    return _default_state_dir() / "skills" / "put-together" / "session.json"


@dataclass(frozen=True)
class Config:
    bridge_url: str
    timeout_seconds: int
    agent_id: str
    agent_name: str
    session_path: Path
    access_token_override: str | None
    refresh_token_override: str | None

    @classmethod
    def from_env(cls) -> "Config":
        bridge_url = os.getenv("PUT_TOGETHER_BRIDGE_URL", "https://put-together-bridge.vercel.app").rstrip("/")
        if not bridge_url:
            raise ValueError("PUT_TOGETHER_BRIDGE_URL is required")

        agent_id = os.getenv("PUT_TOGETHER_AGENT_ID", "").strip() or "openclaw-agent"
        agent_name = os.getenv("PUT_TOGETHER_AGENT_NAME", "").strip() or "Put Together Agent"
        timeout_raw = os.getenv("PUT_TOGETHER_TIMEOUT_SECONDS", "20").strip() or "20"

        try:
            timeout_seconds = int(timeout_raw)
        except ValueError as exc:
            raise ValueError("PUT_TOGETHER_TIMEOUT_SECONDS must be an integer") from exc

        return cls(
            bridge_url=bridge_url,
            timeout_seconds=timeout_seconds,
            agent_id=agent_id,
            agent_name=agent_name,
            session_path=default_session_path(),
            access_token_override=os.getenv("PUT_TOGETHER_ACCESS_TOKEN"),
            refresh_token_override=os.getenv("PUT_TOGETHER_REFRESH_TOKEN"),
        )
