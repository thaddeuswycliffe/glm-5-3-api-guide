# GLM 5.3 API Guide

A focused Argolink guide for **GLM 5.3**: the exact model ID, chat-compatible request, reasoning controls, long-context limits, and production error handling.

[GLM 5.3 model page →](https://argolink.io/gh-glm-5-3-api-guide) · [Argolink API docs →](https://argolink.io/gh-unified-api-docs)

## One working request

```bash
export ARGOLINK_API_KEY='your-key'
curl -sS https://api.argolink.io/v1/chat/completions \
  -H "Authorization: Bearer ${ARGOLINK_API_KEY}" \
  -H 'Content-Type: application/json' \
  -d '{"model":"glm-5.3","messages":[{"role":"user","content":"Compare optimistic and pessimistic locking"}],"reasoning_effort":"max"}'
```

## Model card

- Context window: 1,000,000 tokens; maximum output: 128,000 tokens.
- `reasoning_effort`: `low`, `high`, `max`; default `max`. Thinking is always enabled.
- Current catalog price: $1.40/M input and $4.40/M output; cached input is $0.26/M.

These facts are checked against the current Argolink model page and catalog. See [`argolink/FACTS.md`](argolink/FACTS.md).

## Layout

- `docs/model-card.md`: capability and limit table.
- `docs/api-contract.md`: request, response, and error behavior.
- `glm53_api.py`: small tested Python client.
- `examples/chat.sh`: runnable request.
