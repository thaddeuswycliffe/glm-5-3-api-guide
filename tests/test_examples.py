"""Run the Python examples against a local WSGI stand-in for a GLM endpoint.

Needs `pip install pytest openai`; skipped when the OpenAI SDK is missing.
"""
import importlib.util
import json
import os
import subprocess
import sys
import threading
from wsgiref.simple_server import WSGIRequestHandler, make_server

import pytest

pytestmark = pytest.mark.skipif(importlib.util.find_spec("openai") is None, reason="openai not installed")
EXAMPLES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "examples")


class Quiet(WSGIRequestHandler):
    def log_message(self, *args):
        pass


def glm_app(log):
    def app(environ, start_response):
        size = int(environ.get("CONTENT_LENGTH") or 0)
        body = json.loads(environ["wsgi.input"].read(size))
        log.append(body)
        usage = {"prompt_tokens": 30, "completion_tokens": 120, "total_tokens": 150,
                 "completion_tokens_details": {"reasoning_tokens": 100}}
        if body.get("stream"):
            start_response("200 OK", [("Content-Type", "text/event-stream")])
            deltas = [{"reasoning_content": "hmm"}, {"content": "Idempotent: "}, {"content": "safe to repeat."}]
            events = [{"id": "s", "model": body["model"], "choices": [{"index": 0, "delta": d}]} for d in deltas]
            return [f"data: {json.dumps(e)}\n\n".encode() for e in events] + [b"data: [DONE]\n\n"]
        has_tool_result = any(m.get("role") == "tool" for m in body["messages"])
        if body.get("tools") and not has_tool_result:
            message = {"role": "assistant", "content": "", "reasoning_content": "search first",
                       "tool_calls": [{"id": "call_7", "type": "function", "function": {
                           "name": "search_issues", "arguments": '{"query": "config loader"}'}}]}
        else:
            message = {"role": "assistant", "content": f"{body['model']} says hi", "reasoning_content": "done"}
        payload = {"id": "c", "object": "chat.completion", "created": 0, "model": body["model"], "usage": usage,
                   "choices": [{"index": 0, "message": message,
                                "finish_reason": "tool_calls" if message.get("tool_calls") else "stop"}]}
        start_response("200 OK", [("Content-Type", "application/json")])
        return [json.dumps(payload).encode()]
    return app


@pytest.fixture
def glm():
    log = []
    server = make_server("127.0.0.1", 0, glm_app(log), handler_class=Quiet)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}/v1", log
    server.shutdown()


def run(script, base, *args):
    env = dict(os.environ, GLM_API_KEY="test", GLM_BASE_URL=base)
    done = subprocess.run([sys.executable, os.path.join(EXAMPLES, script), *args],
                          capture_output=True, text=True, env=env, timeout=60)
    assert done.returncode == 0, done.stderr
    return done.stdout


def test_chat_compares_efforts_and_streams(glm):
    base, log = glm
    out = run("chat.py", base)
    assert [b.get("reasoning_effort") for b in log] == ["low", "max", "low"]
    assert "[low] 120 output tokens (100 reasoning)" in out
    assert "Idempotent: safe to repeat." in out and log[2]["stream"] is True


def test_tool_loop_returns_result_and_keeps_reasoning(glm):
    base, log = glm
    out = run("tools.py", base)
    assert "glm-5.3 says hi" in out
    assistant = [m for m in log[1]["messages"] if m["role"] == "assistant"][0]
    assert assistant["reasoning_content"] == "search first" and assistant["tool_calls"][0]["id"] == "call_7"
    tool = [m for m in log[1]["messages"] if m["role"] == "tool"][0]
    assert json.loads(tool["content"])[0]["id"] == 412


def test_flash_gets_the_image(glm):
    base, log = glm
    run("vision_flash.py", base, "https://example.com/a.png")
    parts = log[0]["messages"][0]["content"]
    assert log[0]["model"] == "glm-5.3-flash"
    assert parts[1] == {"type": "image_url", "image_url": {"url": "https://example.com/a.png"}}
