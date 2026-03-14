# Proposed Skill Package Structure

## Package Shape

```text
put-together/
├── SKILL.md
├── .env.example
├── pyproject.toml
├── bridge/
│   └── openapi.yaml
├── references/
│   ├── architecture.md
│   ├── config-and-auth.md
│   ├── distribution.md
│   ├── link-flow.md
│   ├── recommendation-flows.md
│   ├── server-side-boundaries.md
│   └── skill-package-structure.md
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

## Why Each Part Exists

- `SKILL.md`
  - OpenClaw discovery metadata plus the operating rules for the connector
- `.env.example`
  - Minimal bridge configuration template
- `pyproject.toml`
  - Lets the repo be packaged or installed as a Python module later without restructuring
- `bridge/openapi.yaml`
  - Stable bridge contract for the future bridge implementation
- `references/`
  - Implementation-facing docs kept separate from the concise skill instructions
- `scripts/put_together.py`
  - Skill-friendly entrypoint that works from a cloned skill folder
- `src/put_together_skill/`
  - Thin reusable client implementation

## Phase 1 Implementation Rule

If a future contributor wants to add new recommendation types, they should:

1. add a new bridge endpoint to `bridge/openapi.yaml`
2. add one CLI command in `src/put_together_skill/cli.py`
3. document the request shape in `references/`

They should not add local decision logic to the skill package.
