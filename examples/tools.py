"""Function calling with GLM-5.3: the model asks for a tool, we run it, it answers.

    pip install openai
    GLM_API_KEY=... python examples/tools.py
"""
import json
import os

from openai import OpenAI

client = OpenAI(api_key=os.environ["GLM_API_KEY"], base_url=os.environ.get("GLM_BASE_URL", "https://argolink.io/v1"))

TOOLS = [{
    "type": "function",
    "function": {
        "name": "search_issues",
        "description": "Search the issue tracker and return matching issue titles",
        "parameters": {
            "type": "object",
            "properties": {"query": {"type": "string"}, "state": {"type": "string", "enum": ["open", "closed"]}},
            "required": ["query"],
        },
    },
}]


def search_issues(query, state="open"):
    return [{"id": 412, "title": f"{query}: crash on empty config", "state": state}]  # stand-in data


messages = [{"role": "user", "content": "Is there an open issue about the config loader crashing?"}]
for _ in range(4):
    reply = client.chat.completions.create(model="glm-5.3", messages=messages, tools=TOOLS, reasoning_effort="high")
    message = reply.choices[0].message
    messages.append(message)               # keep the whole message, reasoning included
    if not message.tool_calls:
        print(message.content)
        break
    for call in message.tool_calls:
        result = search_issues(**json.loads(call.function.arguments))
        messages.append({"role": "tool", "tool_call_id": call.id, "content": json.dumps(result)})
