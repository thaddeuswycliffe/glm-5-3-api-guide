// GLM-5.3 from Node.js with the OpenAI SDK, streaming the reasoning and the answer separately.
//   npm install openai && GLM_API_KEY=... node examples/stream.mjs
import OpenAI from "openai";

const client = new OpenAI({
  apiKey: process.env.GLM_API_KEY,
  baseURL: process.env.GLM_BASE_URL ?? "https://argolink.io/v1",
});

const stream = await client.chat.completions.create({
  model: "glm-5.3",
  reasoning_effort: "high",
  stream: true,
  messages: [{ role: "user", content: "Sketch a SQL schema for a URL shortener in four tables or fewer." }],
});

let thinking = 0;
for await (const chunk of stream) {
  const delta = chunk.choices[0]?.delta ?? {};
  if (delta.reasoning_content) thinking += delta.reasoning_content.length; // Z.ai's field, outside OpenAI's types
  if (delta.content) process.stdout.write(delta.content);
}
console.log(`\n[${thinking} characters of reasoning streamed before the answer]`);
