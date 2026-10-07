#!/usr/bin/env bash
# GLM-5.3 over plain HTTP: a call at a chosen effort, a stream, and the Anthropic Messages format.
#   GLM_API_KEY=... bash examples/curl.sh
set -euo pipefail
BASE="${GLM_BASE_URL:-https://argolink.io/v1}"
ORIGIN="${BASE%/v1}"

# 1. Chat Completions, Z.ai's native format. Thinking is always on; effort is low | high | max (default max).
curl -sS "$BASE/chat/completions" \
  -H "Authorization: Bearer $GLM_API_KEY" -H "Content-Type: application/json" \
  -d '{
    "model": "glm-5.3",
    "reasoning_effort": "high",
    "max_tokens": 4000,
    "messages": [{"role": "user", "content": "Write a bash one-liner that finds the 5 largest files under the current directory."}]
  }'
echo

# 2. Streaming: reasoning_content deltas arrive before content deltas.
curl -sS -N "$BASE/chat/completions" \
  -H "Authorization: Bearer $GLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "glm-5.3", "reasoning_effort": "low", "stream": true,
       "messages": [{"role": "user", "content": "Name three uses of a bloom filter."}]}'
echo

# 3. Anthropic Messages on the bare origin, the way Claude Code calls it.
curl -sS "$ORIGIN/v1/messages" \
  -H "x-api-key: $GLM_API_KEY" -H "anthropic-version: 2023-06-01" -H "Content-Type: application/json" \
  -d '{"model": "glm-5.3", "max_tokens": 2000, "output_config": {"effort": "high"},
       "messages": [{"role": "user", "content": "Explain a race condition in two sentences."}]}'
echo
