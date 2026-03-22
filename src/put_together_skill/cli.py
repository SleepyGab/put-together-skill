from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from put_together_skill.bridge import BridgeClient, BridgeError
from put_together_skill.config import Config
from put_together_skill.session import Session


def _load_json(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON input: {exc}") from exc
    if not isinstance(parsed, dict):
        raise SystemExit("JSON input must be an object")
    return parsed


def _session_from_config(config: Config) -> Session | None:
    if config.access_token_override and config.refresh_token_override:
        return Session(
            access_token=config.access_token_override,
            refresh_token=config.refresh_token_override,
            expires_at=None,
            linked_user=None,
            agent={
                "id": config.agent_id,
                "name": config.agent_name,
                "platform": "openclaw",
            },
        )
    return Session.load(config.session_path)


def _require_session(config: Config, client: BridgeClient) -> Session:
    session = _session_from_config(config)
    if session is None:
        raise SystemExit("No Put Together session found. Run `link --code ...` first.")

    if session.is_expired():
        if not session.refresh_token:
            raise SystemExit("Put Together session expired and no refresh token is available.")
        session = client.refresh_session(session.refresh_token)
        session.save(config.session_path)
    return session


def _print(payload: dict[str, Any]) -> None:
    sys.stdout.write(json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="put-together")
    subparsers = parser.add_subparsers(dest="command", required=True)

    link = subparsers.add_parser("link", help="Exchange a one-time code for bridge tokens")
    link.add_argument("--code", required=True, help="One-time link code from the Put Together iOS app")

    subparsers.add_parser("status", help="Inspect the current linked session")

    ootd = subparsers.add_parser("ootd", help="Request an outfit-of-the-day recommendation")
    ootd.add_argument("--input", required=True, help="JSON object with OOTD request context")

    style_qa = subparsers.add_parser("style-qa", help="Ask a style question")
    style_qa.add_argument("--question", required=True, help="User's styling question")
    style_qa.add_argument("--input", help="Optional JSON object with additional context")

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        config = Config.from_env()
        client = BridgeClient(config)

        if args.command == "link":
            session = client.link_exchange(args.code)
            session.save(config.session_path)
            _print(
                {
                    "linked": True,
                    "agent": session.agent,
                    "linked_user": session.linked_user,
                    "session_path": str(config.session_path),
                }
            )
            return 0

        session = _require_session(config, client)

        if args.command == "status":
            _print(client.session_status(session.access_token))
            return 0

        if args.command == "ootd":
            payload = _load_json(args.input)
            _print(client.recommendation("/v1/daily-ootd", payload, session.access_token))
            return 0

        if args.command == "style-qa":
            payload = _load_json(args.input)
            payload["question"] = args.question
            _print(client.recommendation("/v1/style-qna", payload, session.access_token))
            return 0

    except BridgeError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1
    except ValueError as exc:
        sys.stderr.write(f"{exc}\n")
        return 1

    sys.stderr.write(f"Unknown command: {args.command}\n")
    return 1
