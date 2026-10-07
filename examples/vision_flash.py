"""Images go to GLM-5.3 Flash or FlashX; GLM-5.3 itself reads text only.

    pip install openai
    GLM_API_KEY=... python examples/vision_flash.py https://example.com/screenshot.png
"""
import os
import sys

from openai import OpenAI

client = OpenAI(api_key=os.environ["GLM_API_KEY"], base_url=os.environ.get("GLM_BASE_URL", "https://argolink.io/v1"))
image_url = sys.argv[1] if len(sys.argv) > 1 else "https://example.com/screenshot.png"

reply = client.chat.completions.create(
    model="glm-5.3-flash",
    reasoning_effort="high",               # Flash runs high or max; low is treated as high on the gateway
    messages=[{"role": "user", "content": [
        {"type": "text", "text": "Describe the layout of this page as a list of components."},
        {"type": "image_url", "image_url": {"url": image_url}},   # a public HTTPS URL or a data: URL
    ]}],
)
print(reply.choices[0].message.content)
