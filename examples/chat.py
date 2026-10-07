"""GLM-5.3 with the OpenAI Python SDK: the same prompt at low and max effort, then a stream.

    pip install openai
    GLM_API_KEY=... python examples/chat.py
"""
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["GLM_API_KEY"], base_url=os.environ.get("GLM_BASE_URL", "https://argolink.io/v1"))
PROMPT = "A function returns the wrong total when two requests update the same cart. Name the bug and the fix."

for effort in ("low", "max"):
    reply = client.chat.completions.create(
        model="glm-5.3",
        messages=[{"role": "user", "content": PROMPT}],
        reasoning_effort=effort,
        max_tokens=8000,                   # caps reasoning and answer together
    )
    details = reply.usage.completion_tokens_details
    reasoning_tokens = getattr(details, "reasoning_tokens", None) if details else None
    print(f"[{effort}] {reply.usage.completion_tokens} output tokens ({reasoning_tokens} reasoning)")
    print(reply.choices[0].message.content, "\n")

stream = client.chat.completions.create(
    model="glm-5.3",
    messages=[{"role": "user", "content": "Give a one-line definition of idempotency."}],
    reasoning_effort="low",
    stream=True,
)
for chunk in stream:
    delta = chunk.choices[0].delta if chunk.choices else None
    if delta is not None and delta.content:
        print(delta.content, end="", flush=True)
print()
