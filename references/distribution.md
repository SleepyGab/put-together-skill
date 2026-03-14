# Trigger, Installation, And Distribution Strategy

## Trigger Strategy

The skill should trigger for language such as:

- "link Put Together"
- "connect my Put Together account"
- "what should I wear today"
- "give me an outfit for a wedding"
- "can I style this with ..."

The SKILL metadata is written so OpenClaw can discover those intent classes.

## Installation Strategy

OpenClaw on this machine currently exposes skill discovery and inspection commands, not a dedicated `skills install` command. It also points users to `clawhub` for search, install, and sync.

Phase 1 recommendation:

1. Ship this repo as a standalone skill folder named `put-together`.
2. Install it by syncing or copying the folder into an OpenClaw-managed skill root such as `~/.openclaw/skills/put-together`.
3. Configure `PUT_TOGETHER_BRIDGE_URL` and agent identity in the OpenClaw runtime environment.
4. Verify with:
   ```bash
   openclaw skills info put-together --json
   openclaw skills check
   ```

## Distribution Options

### Option A: Git-based internal distribution

- Keep this repo private
- Install by cloning into the managed OpenClaw skill directory
- Best for early internal testing

### Option B: Clawhub-managed distribution

- Package the repo for `clawhub` sync/install workflows
- Best once the skill metadata and versioning stabilize

## Versioning

- Version the repo independently from iOS and bridge repos
- Keep bridge API versioned under `/v1`
- Treat any change to request or response contracts as a bridge API change, not a skill-only change

## Phase 1 Packaging Rule

This repo must stay independently shippable. Do not reach into existing Put Together repos at install time. The only runtime dependency should be the configured bridge URL.
