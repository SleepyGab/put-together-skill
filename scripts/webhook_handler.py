#!/usr/bin/env python3
"""
Minimal webhook receiver for Put Together Bridge events.

This script runs a local Flask server that receives webhook events from the
Put Together Bridge when link status changes or daily OOTD recommendations
are generated.

Usage:
    python scripts/webhook_handler.py [--port 8080] [--secret YOUR_SECRET]

Environment variables:
    PUT_TOGETHER_WEBHOOK_SECRET: HMAC secret for verifying webhook signatures
    PUT_TOGETHER_WEBHOOK_PORT: Port to listen on (default: 8080)
"""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer


def verify_signature(payload: bytes, signature: str, secret: str) -> bool:
    """Verify HMAC signature of webhook payload."""
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(expected, signature)


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle incoming webhook POST requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        payload = self.rfile.read(content_length)
        signature = self.headers.get("x-webhook-signature", "")

        secret = os.environ.get("PUT_TOGETHER_WEBHOOK_SECRET", "")
        if secret and not verify_signature(payload, signature, secret):
            self.send_error(401, "Invalid signature")
            return

        try:
            event = json.loads(payload)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        event_type = event.get("event", "unknown")
        print(f"\n=== Webhook Event: {event_type} ===")
        print(json.dumps(event, indent=2, sort_keys=True))
        print()

        if event_type == "link.redeemed":
            print(f"Link {event.get('linkId')} redeemed for user {event.get('putTogetherUserId')}")
        elif event_type == "link.revoked":
            print(f"Link {event.get('linkId')} revoked: {event.get('reason', 'no reason')}")
        elif event_type == "daily_ootd":
            print(f"Daily OOTD for {event.get('putTogetherUserId')} on {event.get('lookDate')}")
            print(f"Summary: {event.get('summary')}")
            if event.get("avatarUrl"):
                print(f"Avatar: {event['avatarUrl']}")
            pieces = event.get("pieces", [])
            if pieces:
                print(f"Pieces: {len(pieces)}")
                for piece in pieces:
                    print(f"  - {piece.get('name')} ({piece.get('category')})")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"ok": true}\n')

    def log_message(self, format, *args):
        """Suppress default HTTP logging."""
        pass


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Put Together webhook receiver")
    parser.add_argument("--port", type=int, default=int(os.environ.get("PUT_TOGETHER_WEBHOOK_PORT", "8080")))
    parser.add_argument("--secret", default=os.environ.get("PUT_TOGETHER_WEBHOOK_SECRET", ""))
    args = parser.parse_args()

    if args.secret:
        os.environ["PUT_TOGETHER_WEBHOOK_SECRET"] = args.secret

    server = HTTPServer(("0.0.0.0", args.port), WebhookHandler)
    print(f"Webhook receiver listening on http://0.0.0.0:{args.port}")
    print("Press Ctrl+C to stop\n")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    sys.exit(main())
