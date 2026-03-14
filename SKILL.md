---
name: put-together
description: Thin OpenClaw connector for Put Together outfit recommendations. Use when linking a user's Put Together account to their OpenClaw agent, getting OOTD recommendations, answering style Q&A, or suggesting occasion-based outfits. Always call the Put Together Bridge service for recommendations; never compute proprietary recommendation logic locally.
---

# Put Together Skill

This skill is an installable OpenClaw package for Put Together. It is intentionally thin.

## Use This Skill For

- Linking an OpenClaw agent to a user's existing Put Together account with a one-time code
- Fetching OOTD recommendations
- Asking style questions grounded in Put Together profile and wardrobe data
- Recommending outfits for an occasion, dress code, weather, or vibe

## Hard Rules

- Treat the bridge as the only network dependency for Phase 1.
- Keep proprietary recommendation logic server-side.
- Do not rank outfits, generate style logic, or infer closet compatibility locally beyond simple request shaping.
- If the user is not linked, stop and ask for a link code from the Put Together iOS app before attempting recommendations.

## Quick Workflow

1. Use the default production bridge configuration (no env required for normal use).
2. Check session status:
   ```bash
   python3 scripts/put_together.py status
   ```
3. If unlinked, redeem the code shown by the iOS app:
   ```bash
   python3 scripts/put_together.py link --code PTB-123456
   ```
4. For recommendations, send the request to the bridge:
   ```bash
   python3 scripts/put_together.py ootd --input '{"weather":{"summary":"65F and sunny"},"context":{"day_type":"workday"}}'
   python3 scripts/put_together.py style-qa --question "Can I wear white sneakers with these trousers?" --input '{"context":{"occasion":"smart casual dinner"}}'
   python3 scripts/put_together.py occasion --input '{"occasion":{"type":"wedding","dress_code":"cocktail"}}'
   ```

## Arguments

- `link`: exchange a one-time code for bridge tokens bound to the agent
- `status`: verify whether the current agent is linked
- `ootd`: request daily outfit recommendations
- `style-qa`: ask a style question; optional supplemental context can be included in `--input`
- `occasion`: request an occasion-specific outfit recommendation

## References

- System design: [references/architecture.md](references/architecture.md)
- Package structure: [references/skill-package-structure.md](references/skill-package-structure.md)
- Link flow: [references/link-flow.md](references/link-flow.md)
- Recommendation request shapes: [references/recommendation-flows.md](references/recommendation-flows.md)
- Env and auth: [references/config-and-auth.md](references/config-and-auth.md)
- Install and distribution: [references/distribution.md](references/distribution.md)
- Server-side boundaries: [references/server-side-boundaries.md](references/server-side-boundaries.md)
- Bridge API contract: [bridge/openapi.yaml](bridge/openapi.yaml)
