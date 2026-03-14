# Phase 1 MVP Architecture

## Goal

Ship a standalone OpenClaw-installable skill package that connects an external OpenClaw agent to Put Together through a dedicated bridge service. The skill is a transport and orchestration layer only. Recommendation logic, ranking, and user-specific style intelligence remain server-side.

## Phase 1 Modules

### 1. Skill Module

Responsibilities:

- Trigger on Put Together intents inside OpenClaw
- Check whether the local agent is linked to a Put Together account
- Exchange a one-time link code for bridge tokens
- Forward OOTD, style Q&A, and occasion payloads to the bridge
- Return bridge responses back to the user cleanly

Non-responsibilities:

- No local recommendation engine
- No local wardrobe ranking
- No direct calls to internal Put Together services
- No web UI

### 2. Put Together Bridge Module

Responsibilities:

- Present a stable public API for skill clients
- Validate one-time link codes issued by the iOS app, backend, or bridge
- Bind an OpenClaw agent identity to a Put Together user
- Normalize skill requests into internal Put Together recommendation calls
- Enforce auth, rate limits, auditing, and response shape consistency

Non-responsibilities:

- No end-user chat UX
- No dependency on OpenClaw internals beyond agent identity metadata

## High-Level Interaction

1. User installs the `put-together` skill into an OpenClaw skill directory.
2. User signs into the existing Put Together iOS app.
3. The app first guides the user to ask their OpenClaw agent to install the public Put Together skill.
4. The app then requests a short-lived one-time link code from Put Together backend or bridge.
5. User gives that code to their OpenClaw agent.
6. The skill redeems the code with the bridge for user-bound bridge credentials.
6. The skill stores only bridge session data locally.
7. Recommendation requests are forwarded to bridge endpoints.
8. The bridge calls internal Put Together services and returns already-ranked results.

## Repo Layout

This repo is designed to ship independently and later wire into the existing Put Together stack:

```text
put-together-skill/
├── SKILL.md
├── .env.example
├── bridge/
│   └── openapi.yaml
├── references/
│   ├── architecture.md
│   ├── config-and-auth.md
│   ├── distribution.md
│   ├── link-flow.md
│   ├── recommendation-flows.md
│   └── server-side-boundaries.md
├── scripts/
│   └── put_together.py
└── src/
    └── put_together_skill/
        ├── __init__.py
        ├── bridge.py
        ├── cli.py
        ├── config.py
        └── session.py
```

## Phase 1 Request Path

```text
OpenClaw Agent
  -> put-together skill
  -> Put Together Bridge
  -> Internal Put Together recommendation services
  -> Put Together Bridge
  -> put-together skill
  -> user
```

## Why This Shape

- The skill can be versioned and shipped without exposing proprietary logic.
- The bridge creates a single compatibility surface for future iOS, OpenClaw, and web clients.
- The internal recommendation system stays replaceable without changing the skill package.
- Auth, logging, and abuse controls are centralized in one place.

## Deferred To Later Phases

- Web connect flow
- Multi-agent linking per user with richer management UI
- Streaming recommendations
- Rich closet editing from OpenClaw
- Push notifications from Put Together to OpenClaw
