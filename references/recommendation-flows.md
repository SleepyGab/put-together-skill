# Recommendation Flows

## Shared Principles

- The skill sends structured context and receives already-computed recommendations.
- The bridge is responsible for profile hydration, closet retrieval, ranking, explanation generation, and policy checks.
- The skill may ask clarifying questions only when required input is missing.

## 1. OOTD Flow

Use when the user wants today's outfit, a quick pick, or a daily recommendation.

Suggested request body:

```json
{
  "context": {
    "day_type": "workday",
    "time_of_day": "morning"
  },
  "weather": {
    "summary": "65F and sunny",
    "temperature_f": 65
  },
  "preferences": {
    "vibe": "polished but easy"
  }
}
```

Suggested response body:

```json
{
  "request_id": "req_ootd_123",
  "recommendations": [
    {
      "look_id": "look_001",
      "title": "Light knit with navy trousers",
      "items": ["cream knit polo", "navy trousers", "white leather sneakers"],
      "why": "Balanced for mild weather and aligned with recent workday preferences."
    }
  ]
}
```

## 2. Style Q&A Flow

Use when the user asks for guidance, compatibility, styling advice, or what to pair with an item.

Suggested request body:

```json
{
  "question": "Can I wear white sneakers with these charcoal trousers?",
  "context": {
    "occasion": "smart casual dinner",
    "photo_ref": null
  }
}
```

Expected bridge behavior:

- Resolve question intent
- Pull relevant profile and wardrobe context
- Return an answer plus recommended pairings when appropriate

## Minimal Skill-Side Validation

- Reject empty requests
- Ensure `question` is present for style Q&A
- Never add hidden recommendation heuristics in the client
