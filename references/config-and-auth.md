# Config And Auth Design

## Required Environment Variables

- `PUT_TOGETHER_BRIDGE_URL`
  - Base URL for the standalone bridge service
  - Defaults to `https://put-together-bridge.vercel.app`
  - Override only if you are testing against a non-production bridge

## Recommended Environment Variables

- `PUT_TOGETHER_AGENT_ID`
  - Stable identifier for the OpenClaw agent or workspace
- `PUT_TOGETHER_AGENT_NAME`
  - Human-friendly label used during linking and audit logs
- `PUT_TOGETHER_TIMEOUT_SECONDS`
  - HTTP timeout for bridge requests
- `PUT_TOGETHER_SESSION_PATH`
  - Override for where bridge session data is stored locally

## Optional Secret Overrides

- `PUT_TOGETHER_ACCESS_TOKEN`
- `PUT_TOGETHER_REFRESH_TOKEN`

These should normally come from the link flow, not manual env configuration.

## Local Session Storage

Default path priority:

1. `PUT_TOGETHER_SESSION_PATH`
2. `$OPENCLAW_STATE_DIR/skills/put-together/session.json`
3. `~/.openclaw/state/skills/put-together/session.json`

Stored fields:

- `access_token`
- `refresh_token`
- `expires_at`
- `linked_user`
- `agent`

## Auth Model

- Phase 1 request auth: bearer access token minted by bridge
- Token refresh: `POST /v1/session/refresh`
- Bridge trust boundary: the bridge maps the token to the linked Put Together user

## Security Notes

- The skill never stores Put Together account credentials.
- The bridge should issue scoped tokens only for bridge APIs.
- Refresh tokens should be revocable independently of the underlying Put Together account session.
- Local session files should be created with user-only permissions where possible.
