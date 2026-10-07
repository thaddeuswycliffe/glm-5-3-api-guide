# GLM-5.3 API guide — from $1.12 per 1M input tokens

**Z.ai GLM-5.3 is live on [ArgoLink](https://argolink.io/gh-glm-5-3-api-guide)**: $1.12 per 1M input tokens, $3.52 per 1M output tokens, $0.208 per 1M cached input tokens, 20% below Z.ai's own price.
GLM-5.3 is Z.ai's flagship for software engineering and long-running agents: 1M-token context, up to 128K output tokens, always-on reasoning at three effort levels, function calling and streaming. The guide also covers the rest of the GLM-5 line: 5.1, 5.2, 5.3 Flash and 5.3 FlashX.

[Model page](https://argolink.io/en/models/glm-5.3) · [At a glance](#at-a-glance) · [Prices](#prices) · [Quick start](#quick-start) · [Reasoning effort](#reasoning-effort-and-thinking) · [FAQ](#faq)

<sub>Last checked: 2026-10-07 against the model pages linked here, Z.ai's docs and pricing page, and OpenRouter's public model data. Unofficial guide; not affiliated with Z.ai or Zhipu.</sub>

## At a glance

| Model ID | Context | Max output | Input | Thinking | `reasoning_effort` (default) | Price per 1M, in / out |
|---|---:|---:|---|---|---|---:|
| `glm-5.3` | 1,000,000 | 128,000 | text | always on | `low` · `high` · `max` (`max`) | $1.12 / $3.52 |
| `glm-5.3-flash` | 1,000,000 | 128,000 | text, images | always on | `high` · `max` (`max`); `low` runs as `high` | $0.12 / $0.40 |
| `glm-5.3-flashx` | 1,000,000 | 128,000 | text, images | always on | `high` · `max` (`max`); `low` runs as `high` | $0.296 / $1.00 |
| `glm-5.2` | 1,000,000 | 128,000 | text | on by default | `high` · `max` (`max`); `none` turns thinking off | $1.12 / $3.52 |
| `glm-5.1` | 200,000 | 128,000 | text | on by default | no levels; `none` turns thinking off | $1.12 / $3.52 |

All five use the same endpoint, `POST https://argolink.io/v1/chat/completions` (Z.ai's own request format); `/v1/responses` and `/v1/messages` are converted to it. Reasoning tokens are billed as output tokens. FlashX is Flash served at about 200 output tokens a second, per Z.ai.

Which one: GLM-5.3 for coding agents and long multi-step work; GLM-5.3 Flash when cost matters or the input has screenshots; FlashX when the same work has to come back faster; GLM-5.2 when you need to switch thinking off.

## Prices

USD per 1M tokens, checked 2026-10-07.

| GLM-5.3 route | Input | Cached input | Output | Notes |
|---|---:|---:|---:|---|
| **[ArgoLink](https://argolink.io/en/models/glm-5.3)** | **$1.12** | **$0.208** | **$3.52** | max output 128,000 |
| [Z.ai](https://docs.z.ai/guides/overview/pricing) (official) | $1.40 | $0.26 | $4.40 | cached-input storage free for a limited time |
| [OpenRouter](https://openrouter.ai/z-ai/glm-5.3), Z.AI route | $1.40 | $0.26 | $4.40 | fp8, max output 131,072 |
| OpenRouter, Together | $1.40 | $0.26 | $4.40 | |
| OpenRouter, Fireworks | $1.40 | $0.26 | $4.40 | |
| OpenRouter, Novita | $0.42 | $0.078 | $1.32 | fp8, max output 131,072 |
| OpenRouter, DeepInfra | $0.5625 | $0.125 | $2.50 | fp4 |
| OpenRouter, all 41 listed routes | $0.063–$2.80 | | $1.32–$8.80 | |

That is 20% under Z.ai's list price and under the full-price routes. OpenRouter also lists cheaper routes, most of them quantized (fp8/fp4). Compare max output and quantization as well as price. The other GLM-5 models, ArgoLink against Z.ai:

| Model | ArgoLink in / cached / out | Z.ai in / cached / out |
|---|---:|---:|
| GLM-5.3 Flash | $0.12 / $0.024 / $0.40 | $0.15 / $0.03 / $0.50 |
| GLM-5.3 FlashX | $0.296 / $0.06 / $1.00 | $0.37 / $0.075 / $1.25 |
| GLM-5.2 | $1.12 / $0.208 / $3.52 | $1.40 / $0.26 / $4.40 |
| GLM-5.1 | $1.12 / $0.208 / $3.52 | $1.40 / $0.26 / $4.40 |

What typical calls cost at the first row's rates:

| Call | GLM-5.3 | GLM-5.3 Flash | GLM-5.3 FlashX |
|---|---:|---:|---:|
| Chat turn, 2,000 in / 800 out | $0.0051 | $0.0006 | $0.0014 |
| Agent turn, 50,000 in (40,000 cached) / 4,000 out | $0.0336 | $0.0038 | $0.0094 |
| Repository review, 600,000 in / 10,000 out | $0.7072 | $0.0760 | $0.1876 |

## Quick start

```bash
export GLM_API_KEY=your-key                 # create one on argolink.io
curl https://argolink.io/v1/chat/completions \
  -H "Authorization: Bearer $GLM_API_KEY" -H "Content-Type: application/json" \
  -d '{"model": "glm-5.3", "reasoning_effort": "high",
       "messages": [{"role": "user", "content": "Review this SQL for injection risks: SELECT * FROM users WHERE id = '\''$id'\''"}]}'
```

```python
import os
from openai import OpenAI

client = OpenAI(api_key=os.environ["GLM_API_KEY"], base_url="https://argolink.io/v1")
reply = client.chat.completions.create(
    model="glm-5.3",
    reasoning_effort="max",          # the default; low and high answer sooner
    max_tokens=16000,                # caps reasoning and answer together
    messages=[{"role": "user", "content": "Plan a zero-downtime migration from Postgres 14 to 17."}],
)
print(getattr(reply.choices[0].message, "reasoning_content", None))  # the reasoning, in Z.ai's format
print(reply.choices[0].message.content)
```

```js
import OpenAI from "openai";

const client = new OpenAI({ apiKey: process.env.GLM_API_KEY, baseURL: "https://argolink.io/v1" });
const reply = await client.chat.completions.create({
  model: "glm-5.3-flash",
  reasoning_effort: "high",
  messages: [{ role: "user", content: "Turn this changelog into release notes: ..." }],
});
console.log(reply.choices[0].message.content);
```

More in [examples/](examples): [curl.sh](examples/curl.sh) (Chat, streaming, Anthropic Messages), [chat.py](examples/chat.py) (low vs max effort, with token counts), [tools.py](examples/tools.py) (a function-calling loop), [vision_flash.py](examples/vision_flash.py) (images on Flash), [stream.mjs](examples/stream.mjs) (Node streaming).

## Reasoning effort and thinking

| | GLM-5.3 | GLM-5.3 Flash / FlashX | GLM-5.2 | GLM-5.1 |
|---|---|---|---|---|
| Thinking | always on | always on | on by default | on by default |
| Effort levels | `low`, `high`, `max` reach the model | `high`, `max`; `low` and `medium` run as `high` | `high`, `max`; `low`/`medium` run as `high`, `xhigh` as `max` | none |
| Turn thinking off (ArgoLink) | not possible; `"none"` is refused | not possible | `reasoning_effort: "none"` | `reasoning_effort: "none"` |
| Turn thinking off (Z.ai) | not possible | not possible | `thinking: {"type": "disabled"}` | `thinking: {"type": "disabled"}` |

Two things catch people out:

- **`thinking.type: "disabled"` is a Z.ai control.** Through `argolink.io` it has no effect on GLM-5.2 and 5.1; send `reasoning_effort: "none"` instead. For GLM-5.3, Z.ai's migration notice says a request with `thinking.type: "disabled"` fails; change it to `reasoning_effort: "low"` before switching model IDs.
- **Effort set on another format may not land.** These controls are documented on Chat Completions. Over `/v1/messages` (Claude Code), effort comes from `output_config.effort`, and the gateway sends `medium` when it is missing, which GLM-5.3 runs as `high`.

## Endpoints and formats

| Format | ArgoLink | Z.ai |
|---|---|---|
| OpenAI Chat Completions | `https://argolink.io/v1/chat/completions`, native | `https://api.z.ai/api/paas/v4/chat/completions` |
| OpenAI Responses | `https://argolink.io/v1/responses`, converted | base URL `https://api.z.ai/api/v1` |
| Anthropic Messages | `https://argolink.io/v1/messages`, converted; SDK base URL `https://argolink.io` | base URL `https://api.z.ai/api/anthropic` |

Web search and other server-side tools are dropped in the Responses and Messages conversions. Images on Flash and FlashX go in as `image_url` parts on Chat Completions; over Messages only base64 images carry over.

## Using GLM-5.3 in coding agents

Claude Code speaks Anthropic Messages, so it needs the bare origin and the GLM model IDs:

```bash
export ANTHROPIC_BASE_URL=https://argolink.io
export ANTHROPIC_AUTH_TOKEN=$GLM_API_KEY
export ANTHROPIC_MODEL=glm-5.3
export ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-5.3-flash   # background tasks use the haiku alias
claude
```

Codex speaks Responses: set `base_url = "https://argolink.io/v1"` and `wire_api = "responses"` in its `model_providers` table. OpenAI-compatible tools such as Cline, OpenCode and Cherry Studio take the `/v1` base URL and the model ID.

## Open weights

GLM-5.3 is also published as open weights: `zai-org/GLM-5.3` on Hugging Face and ModelScope, 744B parameters with 40B active, in FP8 and BF16; GLM-5.3 Flash is 320B with 18B active. Z.ai's [GLM-5 repository](https://github.com/zai-org/GLM-5) links serving recipes for vLLM, SGLang, KTransformers and Transformers. At that size, self-hosting means a multi-GPU node; per-token APIs are the practical choice below steady high volume.

## What Z.ai reports

Vendor-reported results from Z.ai's [GLM-5.3 page](https://docs.z.ai/guides/llm/glm-5.3), not independently verified:

| Benchmark | GLM-5.2 | GLM-5.3 |
|---|---:|---:|
| Terminal-Bench 3.0 | 4.6 | 28.3 |
| DeepSWE v1.1 | 46.2 | 66.9 |
| Agents' Last Exam | 23.8 | 28.5 |

Z.ai also reports a 50% gain over GLM-5.2 on its in-house Z.ai Code Bench, with fewer output tokens per task at the same effort level.

## FAQ

**What is the GLM-5.3 model ID?**
`glm-5.3`, the same on both hosts above. The siblings are `glm-5.3-flash`, `glm-5.3-flashx`, `glm-5.2` and `glm-5.1`.

**How much does GLM-5.3 cost per million tokens?**
$1.12 input, $0.208 cached input and $3.52 output on ArgoLink; $1.40, $0.26 and $4.40 at Z.ai. Reasoning tokens are output tokens, so `max` effort costs more per answer than `low`.

**Can GLM-5.3 read images?**
No, it reads text only. Use `glm-5.3-flash` or `glm-5.3-flashx`, which take images as `image_url` parts.

**How do I make GLM-5.3 answer faster?**
Send `reasoning_effort: "low"` and stream. Thinking can't be switched off on GLM-5.3. If you need a model without reasoning, GLM-5.2 with `reasoning_effort: "none"` is one; GLM-5.3 FlashX is the fastest of the line.

**Does GLM-5.3 support function calling and JSON output?**
Z.ai lists function calling, streaming, context caching and structured output for GLM-5.3. Tool calls work on Chat Completions as shown in [tools.py](examples/tools.py).

**Is the context really 1M tokens?**
1,000,000 tokens for GLM-5.3, 5.3 Flash, 5.3 FlashX and 5.2; GLM-5.1 has 200,000. Output is capped at 128,000 tokens for all five.

## Tests

```bash
pip install pytest openai
pytest tests/
```

The tests run `chat.py`, `tools.py` and `vision_flash.py` against a local stand-in server and check the requests they send, so they need no key.

## License

MIT
