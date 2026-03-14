# Server-Side Boundaries

## What Must Stay In Put Together Systems

- Closet retrieval and normalization
- User profile interpretation
- Style preference inference
- Recommendation ranking logic
- Explanation generation based on proprietary signals
- Guardrails and business rules
- Telemetry and experimentation logic

## What The Skill May Do

- Collect user intent and optional structured context
- Exchange link codes for bridge tokens
- Forward requests to the bridge
- Render bridge responses in a conversational format
- Surface recoverable errors cleanly

## Explicit Non-Goals For The Skill

- No local fallback recommendation engine
- No embedding of ranking weights or decision trees
- No caching of closet inventories beyond transient request context unless explicitly added later
- No direct knowledge of private Put Together internal APIs

## Contract Discipline

If the bridge changes its internal logic, the skill should keep working as long as:

- endpoint paths stay stable
- auth semantics stay stable
- response contracts remain backward compatible

That is the core reason to keep the skill thin.
