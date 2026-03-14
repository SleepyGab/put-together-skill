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

Phase 1 recommendation:

1. Ship this repo as a standalone public skill folder named `put-together`.
2. Install it by cloning or syncing the repo into an OpenClaw-managed skill root such as `~/.openclaw/skills/put-together`.
3. Use the default production bridge URL unless you are deliberately testing against a staging bridge.
4. Verify with:
   ```bash
   openclaw skills info put-together --json
   openclaw skills check
   ```

Public repo:
- `https://github.com/SleepyGab/put-together-skill`

## Distribution Options

### Option A: Public Git-based distribution

- Install from the public GitHub repo
- Best for current testing because bridge URL now defaults to production

### Option B: Clawhub-managed distribution

- Package the repo for `clawhub` sync/install workflows
- Best once the skill metadata and versioning stabilize

## Versioning

- Version the repo independently from iOS and bridge repos
- Keep bridge API versioned under `/v1`
- Treat any change to request or response contracts as a bridge API change, not a skill-only change

## Phase 1 Packaging Rule

This repo must stay independently shippable. Do not reach into existing Put Together repos at install time. The only runtime dependency should be the configured bridge URL.
