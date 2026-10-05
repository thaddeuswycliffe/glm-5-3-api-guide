#!/usr/bin/env bash
set -euo pipefail
: "${ARGOLINK_API_KEY:?set ARGOLINK_API_KEY first}"
curl -sS "${ARGOLINK_BASE_URL:-https://api.argolink.io}/v1/chat/completions" \
  -H "Authorization: Bearer ${ARGOLINK_API_KEY}" -H 'Content-Type: application/json' \
  -d '{"model":"glm-5.3","messages":[{"role":"user","content":"Write a concise migration checklist"}],"reasoning_effort":"max"}'
