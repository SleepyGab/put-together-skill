# Link Flow Design

## Objective

Link a user's external OpenClaw agent to their existing Put Together account without exposing internal credentials to the skill package.

## Link Code Pattern

- Format: short human-enterable code such as `PT-ABCD1234`
- Lifetime: 10 minutes
- Usage count: one successful exchange only
- Scope: link a single OpenClaw agent to a single Put Together user

## Sequence

1. User opens the Put Together iOS app and taps `Connect OpenClaw`.
2. The app calls Put Together backend or the bridge to mint a one-time link code for the signed-in user.
3. Backend persists:
   - `code`
   - `user_id`
   - `expires_at`
   - `issued_by`
   - optional `allowed_agent_id`
4. The app shows the code to the user.
5. The user tells their OpenClaw agent to link using that code.
6. The skill calls `POST /v1/link/exchange` with:
   - `code`
   - `agent.id`
   - `agent.name`
   - `agent.platform = openclaw`
7. The bridge validates the code, binds the agent, invalidates the code, and returns:
   - `access_token`
   - `refresh_token`
   - `expires_in`
   - `linked_user` summary
8. The skill stores the session locally and uses the access token for later recommendation calls.

## Why Code Exchange Instead Of Direct Login

- Avoids embedding Put Together user credentials in OpenClaw
- Keeps the existing iOS app as the trusted entry point
- Lets the bridge own token minting, revocation, and audit logs
- Keeps OpenClaw installation simple for Phase 1

## Failure Cases

- Expired code: prompt user to generate a new code in the iOS app
- Reused code: reject and generate a new code
- Agent mismatch: reject if the code is pre-bound to a different agent identity
- Bridge unavailable: do not retry indefinitely; surface a temporary outage message

## Recommended Bridge Rules

- Store hashed link codes at rest
- Rate limit exchange attempts per code and per source IP
- Include `linked_at`, `last_used_at`, and `revoked_at` fields in the agent linkage record
- Support server-side unlink and token revocation later without changing the skill surface
